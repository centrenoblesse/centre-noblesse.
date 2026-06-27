from flask import Blueprint, request, jsonify, current_app
from app.models import UserRegistration, Appointment, db
from datetime import datetime

api_bp = Blueprint('api', __name__)


@api_bp.after_request
def add_no_cache_headers(response):
    """Force browsers and proxies to never cache any API response."""
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


@api_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    try:
        reg = UserRegistration(
            student_name=data.get('name'),
            phone_number=data.get('phone'),
            email_address=data.get('email'),
            selected_service=data.get('course'),
            message=data.get('msg', '')
        )
        db.session.add(reg)
        db.session.commit()
        # TODO: Send email
        return jsonify({"status": "success", "message": "Registration logged."}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@api_bp.route('/appointment', methods=['POST'])
def appointment():
    data = request.json
    try:
        app_req = Appointment(
            name=data.get('name'),
            phone_number=data.get('phone'),
            appointment_date=data.get('date'),
            reason=data.get('reason')
        )
        db.session.add(app_req)
        db.session.commit()
        # TODO: Send email
        return jsonify({"status": "success", "message": "Appointment logged."}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
@api_bp.route('/catalog', methods=['GET'])
def get_catalog():
    from app.models import Category, Service
    categories = Category.query.all()
    services = Service.query.filter_by(status='published', is_pack=False).order_by(Service.sort_order).all()
    
    cat_data = [{"id": c.id, "name": c.name, "slug": c.slug} for c in categories]
    srv_data = [{
        "id": s.id,
        "title": s.title,
        "category_id": s.category_id,
        "price": s.price,
        "description": s.description,
        "status": s.status,
        "sort_order": s.sort_order
    } for s in services]

    resp = jsonify({
        "categories": cat_data,
        "services": srv_data
    })
    resp.status_code = 200
    # Force browsers and proxies to never cache the live catalog
    resp.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    resp.headers['Pragma'] = 'no-cache'
    resp.headers['Expires'] = '0'
    return resp

@api_bp.route('/packs', methods=['GET'])
def get_packs():
    from app.models import Service
    packs = Service.query.filter_by(status='published', is_pack=True).order_by(Service.sort_order).all()
    
    pack_data = [{
        "id": p.id,
        "title": p.title,
        "description": p.description,
        "price": p.price,
        "status": p.status,
        "badge_label": p.badge_label,
        "original_price": p.original_price,
        "savings": p.savings,
        "duration": p.duration,
        "included_courses": p.included_courses.split('\n') if p.included_courses else [],
        "category_id": p.category_id
    } for p in packs]

    resp = jsonify({"packs": pack_data})
    resp.status_code = 200
    resp.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    resp.headers['Pragma'] = 'no-cache'
    resp.headers['Expires'] = '0'
    return resp

@api_bp.route('/reset_db_fix', methods=['GET'])
def reset_db_fix():
    """Endpoint to trigger the DB seed from the web to guarantee UTF-8 encoding in SQLite"""
    try:
        import sys
        sys.path.append(current_app.root_path)
        from seed_db import seed_data
        seed_data()
        return jsonify({"status": "success", "message": "Database successfully re-seeded with perfect UTF-8 characters! Refresh your website."}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
