import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv

load_dotenv()

# Extensions
db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-please-change-in-prod')
    
    # Render provides postgres:// but SQLAlchemy requires postgresql://
    db_url = os.environ.get('DATABASE_URL', 'sqlite:///noblesse.db')
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
        
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Init Extensions
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    csrf.init_app(app)
    
    login_manager.login_view = 'admin.login'
    login_manager.login_message_category = 'info'
    
    # Register Blueprints
    from app.routes.admin import admin_bp
    from app.routes.public import public_bp
    from app.routes.api import api_bp
    
    app.register_blueprint(admin_bp)
    app.register_blueprint(public_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Exempt API from CSRF so that public fetch requests do not fail
    csrf.exempt(api_bp)
    
    return app
