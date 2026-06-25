from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app.models import Admin, Category, Service, SiteSetting, ActivityLog, db
from app import bcrypt

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Detect AJAX calls from the hidden gateway modal
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if current_user.is_authenticated:
        if is_ajax:
            return jsonify({"status": "success", "redirect": url_for('admin.dashboard')})
        return redirect(url_for('admin.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        user = Admin.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user)
            log = ActivityLog(admin_id=user.id, action="Logged in")
            db.session.add(log)
            db.session.commit()
            if is_ajax:
                return jsonify({"status": "success", "redirect": url_for('admin.dashboard')})
            return redirect(url_for('admin.dashboard'))
        else:
            if is_ajax:
                return jsonify({"status": "error", "message": "Identifiants ou code d'acc�s invalides."}), 401
            flash('Identifiants incorrects. Veuillez v�rifier votre nom et code d\'acc�s.', 'danger')

    return render_template('admin/login.html')

@admin_bp.route('/logout')
@login_required
def logout():
    log = ActivityLog(admin_id=current_user.id, action="Logged out")
    db.session.add(log)
    db.session.commit()
    logout_user()
    return redirect(url_for('admin.login'))

@admin_bp.route('/')
@admin_bp.route('/dashboard')
@login_required
def dashboard():
    services_count = Service.query.count()
    categories_count = Category.query.count()
    logs = ActivityLog.query.order_by(ActivityLog.timestamp.desc()).limit(10).all()
    return render_template('admin/dashboard.html', 
                           services_count=services_count, 
                           categories_count=categories_count,
                           logs=logs)

from slugify import slugify

@admin_bp.route('/categories', methods=['GET', 'POST'])
@login_required
def categories():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        if name:
            slug = slugify(name)
            cat = Category(name=name, slug=slug, description=description)
            db.session.add(cat)
            db.session.add(ActivityLog(admin_id=current_user.id, action=f"Created category: {name}"))
            db.session.commit()
            flash('Cat�gorie ajout�e avec succ�s', 'success')
        return redirect(url_for('admin.categories'))
        
    categories_list = Category.query.all()
    return render_template('admin/categories.html', categories=categories_list)

@admin_bp.route('/categories/delete/<int:id>', methods=['POST'])
@login_required
def delete_category(id):
    cat = Category.query.get_or_404(id)
    name = cat.name
    db.session.delete(cat)
    db.session.add(ActivityLog(admin_id=current_user.id, action=f"Deleted category: {name}"))
    db.session.commit()
    flash('Cat�gorie supprim�e.', 'success')
    return redirect(url_for('admin.categories'))

@admin_bp.route('/services', methods=['GET', 'POST'])
@login_required
def services():
    if request.method == 'POST':
        title = request.form.get('title')
        category_id = request.form.get('category_id')
        description = request.form.get('description')
        price = request.form.get('price')
        status = request.form.get('status')
        if title:
            srv = Service(title=title, category_id=category_id, description=description, price=price, status=status)
            db.session.add(srv)
            db.session.add(ActivityLog(admin_id=current_user.id, action=f"Created service: {title}"))
            db.session.commit()
            flash('Service ajout� avec succ�s', 'success')
        return redirect(url_for('admin.services'))
        
    services_list = Service.query.order_by(Service.sort_order).all()
    categories_list = Category.query.all()
    return render_template('admin/services.html', services=services_list, categories=categories_list)

@admin_bp.route('/services/delete/<int:id>', methods=['POST'])
@login_required
def delete_service(id):
    srv = Service.query.get_or_404(id)
    title = srv.title
    db.session.delete(srv)
    db.session.add(ActivityLog(admin_id=current_user.id, action=f"Deleted service: {title}"))
    db.session.commit()
    flash('Service supprim�.', 'success')
    return redirect(url_for('admin.services'))

@admin_bp.route('/services/toggle/<int:id>', methods=['POST'])
@login_required
def toggle_service(id):
    srv = Service.query.get_or_404(id)
    srv.status = 'draft' if srv.status == 'published' else 'published'
    db.session.add(ActivityLog(admin_id=current_user.id, action=f"Toggled service status: {srv.title} to {srv.status}"))
    db.session.commit()
    flash(f'Service {srv.status}.', 'success')
    return redirect(url_for('admin.services'))

@admin_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        for key, value in request.form.items():
            setting = SiteSetting.query.get(key)
            if setting:
                setting.value = value
            else:
                setting = SiteSetting(key=key, value=value)
                db.session.add(setting)
        db.session.add(ActivityLog(admin_id=current_user.id, action="Updated website settings"))
        db.session.commit()
        flash('Param�tres mis � jour.', 'success')
        return redirect(url_for('admin.settings'))
        
    settings_list = SiteSetting.query.all()
    settings_dict = {s.key: s.value for s in settings_list}
    return render_template('admin/settings.html', settings=settings_dict)
