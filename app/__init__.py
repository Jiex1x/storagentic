from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    from .core import bp as core_bp
    app.register_blueprint(core_bp)
    
    return app 