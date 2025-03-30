from flask import Blueprint

bp = Blueprint('core', __name__, 
    template_folder='../templates',
    static_folder='../static'
)

from . import routes

def init_app(app):
    app.register_blueprint(bp)

# Import routes after blueprint creation to avoid circular imports
from . import routes 