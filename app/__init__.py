# -*- coding: utf-8 -*-
import os
import time
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS
from dotenv import load_dotenv

# Force UTF-8 at the Python I/O level for the entire process
os.environ.setdefault('PYTHONIOENCODING', 'utf-8')
os.environ.setdefault('LANG', 'en_US.UTF-8')
os.environ.setdefault('LC_ALL', 'en_US.UTF-8')

load_dotenv()

# Extensions
db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)

    # Force UTF-8 natively — prevents French accents from escaping in JSON
    app.json.ensure_ascii = False

    # Cache-busting version token — changes on every restart, forcing browsers
    # to drop stale CSS/JS. Use in templates as: ?v={{ config.ASSET_VERSION }}
    app.config['ASSET_VERSION'] = str(int(time.time()))

    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-please-change-in-prod')
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    
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
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
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

    @app.after_request
    def enforce_utf8_mime(response):
        """Ensure CSS and JS files are served with explicit UTF-8 charset.
        This prevents browsers from misinterpreting French accents/emojis."""
        content_type = response.content_type
        if 'text/css' in content_type and 'charset' not in content_type:
            response.content_type = 'text/css; charset=utf-8'
        elif 'text/javascript' in content_type and 'charset' not in content_type:
            response.content_type = 'text/javascript; charset=utf-8'
        elif 'text/html' in content_type and 'charset' not in content_type:
            response.content_type = 'text/html; charset=utf-8'
        return response

    return app
