from flask import Flask, jsonify, render_template_string
import threading
import time
import random

# Tente importar o scapy. Se falhar ou estiver no notebook, ative o Mock automaticamente.
try:
    from scapy.all import sniff, Dot11ProbeReq, Dot11Beacon
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False

app = Flask(__name__)

# Configurações do CIVOPS Radar
MOCK_MODE = not SCAPY_AVAILABLE # Mude para False no Raspberry Pi se quiser forçar o hardware
INTERFACE = "wlan0" # Interface em Monitor Mode no Pi (pode ser wlan0mon dependendo do setup)

# Dicionário em memória para armazenar os alvos detectados: { "MAC": {"rssi": -60, "last_seen": timestamp} }
targets = {}

def calculate_distance(rssi):
    """
    Fórmula básica de Path Loss. 
    Ajuste o tx_power e o n (fator de atenuação ambiental) conforme testes em campo.
    """
    tx_power = -40 # Sinal de referência a 1 metro de distância
    n = 2.5 # Fator de ambiente (2.0 a 4.0 dependendo de obstáculos)
    distance = 10 ** ((tx_power - rssi) / (10 * n))
    return round(distance, 2)

def packet_handler(pkt):
    """ Callback do Scapy para cada pacote capturado """
    if pkt.haslayer(Dot11ProbeReq) or pkt.haslayer(Dot11Beacon):
        mac = pkt.addr2
        try:
            # Extrai o RSSI dos metadados do pacote de rádio
            rssi = pkt.dBm_AntSignal
        except AttributeError:
            rssi = -90 # Valor default caso o hardware não reporte o RSSI
        
        if mac:
            targets[mac] = {
                "rssi": rssi,
                "distance": calculate_distance(rssi),
                "last_seen": time.time()
            }

def sniffer_thread():
    """ Roda em segundo plano capturando os pacotes reais """
    print(f"[*] Iniciando captura real na interface {INTERFACE}...")
    sniff(iface=INTERFACE, prn=packet_handler, store=False)

def mock_thread():
    """ Roda no seu notebook gerando dados falsos para debugar o front-end """
    print("[!] Rodando em MOCK_MODE. Gerando dados falsos...")
    while True:
        mock_mac = f"00:11:22:33:44:{random.randint(10, 99)}"
        mock_rssi = random.randint(-90, -30)
        targets[mock_mac] = {
            "rssi": mock_rssi,
            "distance": calculate_distance(mock_rssi),
            "last_seen": time.time()
        }
        time.sleep(1) # Simula a detecção de um dispositivo a cada segundo

@app.route('/api/targets')
def get_targets():
    """ Endpoint que o JavaScript do celular vai chamar para atualizar o HUD """
    current_time = time.time()
    active_targets = []
    
    # Limpa dispositivos que não são vistos há mais de 30 segundos e formata a saída
    keys_to_delete = []
    for mac, data in targets.items():
        if current_time - data["last_seen"] > 30:
            keys_to_delete.append(mac)
        else:
            active_targets.append({
                "mac": mac,
                "rssi": data["rssi"],
                "distance": data["distance"]
            })
            
    for key in keys_to_delete:
        del targets[key]
        
    return jsonify(active_targets)

@app.route('/')
def index():
    """ Serve a interface visual (HUD) """
    # Para facilitar, você pode colocar o HTML num arquivo separado "templates/index.html"
    # e usar render_template('index.html')
    return render_template_string("<h1>CIVOPS Radar Online</h1><p>Acesse /api/targets para ver os dados.</p>")

if __name__ == '__main__':
    # Inicia a thread de captura de rádio antes de subir o servidor web
    if MOCK_MODE:
        t = threading.Thread(target=mock_thread, daemon=True)
    else:
        t = threading.Thread(target=sniffer_thread, daemon=True)
    t.start()
    
    # Roda o Flask escutando em todas as interfaces no IP do túnel Bluetooth
    # No seu notebook, acesse http://localhost:5000
    app.run(host='0.0.0.0', port=5000, debug=False)