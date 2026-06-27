from flask import Blueprint, render_template
from app.models import Category, Service, SiteSetting

public_bp = Blueprint('public', __name__)

@public_bp.context_processor
def inject_settings():
    settings = {s.key: s.value for s in SiteSetting.query.all()}
    return dict(settings=settings)

@public_bp.route('/')
def index():
    services = Service.query.filter_by(status='published').order_by(Service.sort_order).all()
    categories = Category.query.all()
    return render_template('public/index.html', services=services, categories=categories)

@public_bp.route('/categories')
def categories():
    categories = Category.query.all()
    services = Service.query.filter_by(status='published').order_by(Service.sort_order).all()
    return render_template('public/categories.html', categories=categories, services=services)

@public_bp.route('/noblesse-cms')
@public_bp.route('/admin-dashboard')
def cms_direct():
    from flask import redirect, url_for
    return redirect(url_for('admin.login'))
