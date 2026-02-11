from flask import Blueprint, jsonify, render_template_string, render_template    
from radar.application.services import TargetService

# Blueprint instead of app to allow better organization if needed
api_bp = Blueprint('api', __name__)

# We need a way to inject the service. For simplicity in Flask without a DI framework,
# we'll attach it to the app config or use a global context, or pass it to the create_app.
# However, usually blueprints are registered and they need access to the service.
# A common pattern is to stash the service in `current_app.config` or similar.

def configure_routes(app, target_service: TargetService):
    
    @app.route('/api/targets')
    def get_targets():
        return jsonify(target_service.get_active_targets())

    @app.route('/')
    def index():
        return render_template('index.html')
