from app import create_app, db
from app.models import Category, Service
from slugify import slugify

app = create_app()

def seed_data():
    with app.app_context():
        # Clear existing data to avoid duplicates if run multiple times
        Service.query.delete()
        Category.query.delete()
        
        categories_data = {
            "Informatique": [
                {"title": "Introduction à l'Informatique", "price": "6 000 DA", "desc": "Durée: 16h. Initiation aux bases de l'informatique."},
                {"title": "Agent de Saisie", "price": "12 000 DA", "desc": "Durée: 40h. Formation complète en bureautique."},
                {"title": "Python", "price": "8 000 DA", "desc": "Durée: 24h. Programmation et développement."},
                {"title": "Langage C / C++ / Java", "price": "8 000 DA", "desc": "Durée: 24h / module."},
                {"title": "Design UI/UX", "price": "10 000 DA", "desc": "Durée: 24h. Web Design et prototypage."},
                {"title": "Front-End (HTML/CSS/JS)", "price": "15 000 DA", "desc": "Durée: 24h. Développement Web Frontend."},
                {"title": "Back-End & Base de Données", "price": "25 000 DA", "desc": "Durée: 48h. Développement Web Backend."},
                {"title": "Initiation Cybersécurité / IA", "price": "25 000 DA", "desc": "Durée: 50h. Nouvelles Technologies."}
            ],
            "Training of Trainers & PNL": [
                {"title": "Prise de Parole Publique", "price": "9 000 DA", "desc": "Durée: 16h. Soft Skills."},
                {"title": "Self Marketing", "price": "12 000 DA", "desc": "Durée: 24h. Développement Professionnel."},
                {"title": "PNL Niveau 1", "price": "15 000 DA", "desc": "Durée: 24h. Psychologie et communication."}
            ],
            "Marketing Digital": [
                {"title": "Marketing Digital", "price": "15 000 DA", "desc": "Durée: 24h. Stratégies digitales."},
                {"title": "Community Management", "price": "12 000 DA", "desc": "Durée: 24h. Gestion des réseaux sociaux."}
            ],
            "Langues": [
                {"title": "Anglais", "price": "10 000 DA", "desc": "Durée: 40h / niveau. Linguistique."},
                {"title": "Français", "price": "10 000 DA", "desc": "Durée: 40h / niveau. Linguistique."},
                {"title": "Espagnol", "price": "10 000 DA", "desc": "Durée: 40h / niveau. Linguistique."},
                {"title": "Italien", "price": "10 000 DA", "desc": "Durée: 40h / niveau. Linguistique."},
                {"title": "Allemand", "price": "10 000 DA", "desc": "Durée: 40h / niveau. Linguistique."},
                {"title": "Russe", "price": "10 000 DA", "desc": "Durée: 40h / niveau. Linguistique."},
                {"title": "Arabe", "price": "10 000 DA", "desc": "Durée: 40h / niveau. Linguistique."}
            ],
            "Kids Program": [
                {"title": "Soroban (Calcul Mental)", "price": "9 000 DA", "desc": "Développement Mental. Par niveau."},
                {"title": "Jeu d'Échecs / Rubik's Cube", "price": "3 000 DA / mois", "desc": "Logique & Stratégie."},
                {"title": "Robotique pour Enfants", "price": "12 000 DA", "desc": "Technologie et apprentissage par le jeu."}
            ],
            "Formations Divers": [
                {"title": "Canva / Illustrator / Photoshop", "price": "6 000 DA", "desc": "Durée: 16h / logiciel. Design Graphique."},
                {"title": "R — Statistiques / LaTeX / Matlab", "price": "4 000 DA", "desc": "Durée: 16h à 24h. Statistiques & Calcul."},
                {"title": "Introduction Photo / Montage Vidéo", "price": "6 000 DA", "desc": "Durée: 16h / module. Audiovisuel."}
            ]
        }
        
        for cat_name, services in categories_data.items():
            cat = Category(name=cat_name, slug=slugify(cat_name), description=f"Cours de {cat_name}")
            db.session.add(cat)
            db.session.flush() # To get cat.id
            
            for s in services:
                srv = Service(
                    title=s['title'],
                    description=s['desc'],
                    price=s['price'],
                    category_id=cat.id,
                    status='published'
                )
                db.session.add(srv)
                
        db.session.commit()
        print("Database seeded with original content!")

if __name__ == '__main__':
    seed_data()
