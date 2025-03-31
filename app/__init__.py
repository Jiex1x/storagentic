from flask import Flask
from flask_cors import CORS
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    CORS(app)  # 启用 CORS 支持
    app.config.from_object(config_class)

    # 注册蓝图
    from app.core import bp as core_bp
    app.register_blueprint(core_bp)

    return app 