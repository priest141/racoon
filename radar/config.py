import os

class Config:
    INTERFACE = os.getenv("RADAR_INTERFACE", "wlan0")
    # Mude para False no Raspberry Pi se quiser forçar o hardware, ou use a variável de ambiente
    MOCK_MODE = os.getenv("RADAR_MOCK_MODE", "True").lower() == "true"
    
    # Configurações de Path Loss para cálculo de distância
    TX_POWER = -40  # Sinal de referência a 1 metro de distância
    ENV_FACTOR = 2.5 # Fator de ambiente (2.0 a 4.0 dependendo de obstáculos)
    
    # Tempo em segundos para considerar um alvo inativo
    TARGET_TIMEOUT = 30
