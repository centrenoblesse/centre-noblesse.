from app import create_app, db, bcrypt
from app.models import Admin, SiteSetting

app = create_app()

def init():
    with app.app_context():
        db.create_all()
        
        # Create default admin if not exists
        if not Admin.query.filter_by(username='admin').first():
            hashed_password = bcrypt.generate_password_hash('password123').decode('utf-8')
            admin = Admin(username='admin', email='admin@noblesse.dz', password_hash=hashed_password)
            db.session.add(admin)
            print("Default admin created (admin / password123)")
            
        # Create default settings
        default_settings = [
            ('site_title', 'Centre Noblesse School'),
            ('site_description', 'Formation professionnelle d\'excellence'),
            ('contact_phone', '+213 123 456 789'),
            ('contact_email', 'contact@noblesse.dz'),
            ('contact_address', 'Algérie'),
            ('hero_title', 'Réveillez le Génie qui est en vous !'),
            ('hero_subtitle', 'Développez vos compétences avec les meilleurs experts.')
        ]
        
        for key, value in default_settings:
            if not SiteSetting.query.get(key):
                setting = SiteSetting(key=key, value=value)
                db.session.add(setting)
                
        db.session.commit()
        print("Database initialized successfully.")

if __name__ == '__main__':
    init()
