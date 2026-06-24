from flask import Blueprint, request, jsonify
from app.models import UserRegistration, Appointment, db
from datetime import datetime

api_bp = Blueprint('api', __name__)

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
    services = Service.query.filter_by(status='published').order_by(Service.sort_order).all()
    
    cat_data = [{"id": c.id, "name": c.name, "slug": c.slug} for c in categories]
    srv_data = [{"id": s.id, "title": s.title, "category_id": s.category_id, "price": s.price, "description": s.description} for s in services]
    
    return jsonify({
        "categories": cat_data,
        "services": srv_data
    }), 200
