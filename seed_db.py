# -*- coding: utf-8 -*-
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
                {"title": "Introduction � l'Informatique", "price": "6 000 DA", "desc": "Dur�e: 16h. Initiation aux bases de l'informatique."},
                {"title": "Agent de Saisie", "price": "12 000 DA", "desc": "Dur�e: 40h. Formation compl�te en bureautique."},
                {"title": "Python", "price": "8 000 DA", "desc": "Dur�e: 24h. Programmation et d�veloppement."},
                {"title": "Langage C / C++ / Java", "price": "8 000 DA", "desc": "Dur�e: 24h / module."},
                {"title": "Design UI/UX", "price": "10 000 DA", "desc": "Dur�e: 24h. Web Design et prototypage."},
                {"title": "Front-End (HTML/CSS/JS)", "price": "15 000 DA", "desc": "Dur�e: 24h. D�veloppement Web Frontend."},
                {"title": "Back-End & Base de Donn�es", "price": "25 000 DA", "desc": "Dur�e: 48h. D�veloppement Web Backend."},
                {"title": "Initiation Cybers�curit� / IA", "price": "25 000 DA", "desc": "Dur�e: 50h. Nouvelles Technologies."}
            ],
            "Training of Trainers & PNL": [
                {"title": "Prise de Parole Publique", "price": "9 000 DA", "desc": "Dur�e: 16h. Soft Skills."},
                {"title": "Self Marketing", "price": "12 000 DA", "desc": "Dur�e: 24h. D�veloppement Professionnel."},
                {"title": "PNL Niveau 1", "price": "15 000 DA", "desc": "Dur�e: 24h. Psychologie et communication."}
            ],
            "Marketing Digital": [
                {"title": "Marketing Digital", "price": "15 000 DA", "desc": "Dur�e: 24h. Strat�gies digitales."},
                {"title": "Community Management", "price": "12 000 DA", "desc": "Dur�e: 24h. Gestion des r�seaux sociaux."}
            ],
            "Langues": [
                {"title": "Anglais", "price": "10 000 DA", "desc": "Dur�e: 40h / niveau. Linguistique."},
                {"title": "Fran�ais", "price": "10 000 DA", "desc": "Dur�e: 40h / niveau. Linguistique."},
                {"title": "Espagnol", "price": "10 000 DA", "desc": "Dur�e: 40h / niveau. Linguistique."},
                {"title": "Italien", "price": "10 000 DA", "desc": "Dur�e: 40h / niveau. Linguistique."},
                {"title": "Allemand", "price": "10 000 DA", "desc": "Dur�e: 40h / niveau. Linguistique."},
                {"title": "Russe", "price": "10 000 DA", "desc": "Dur�e: 40h / niveau. Linguistique."},
                {"title": "Arabe", "price": "10 000 DA", "desc": "Dur�e: 40h / niveau. Linguistique."}
            ],
            "Kids Program": [
                {"title": "Soroban (Calcul Mental)", "price": "9 000 DA", "desc": "D�veloppement Mental. Par niveau."},
                {"title": "Jeu d'�checs / Rubik's Cube", "price": "3 000 DA / mois", "desc": "Logique & Strat�gie."},
                {"title": "Robotique pour Enfants", "price": "12 000 DA", "desc": "Technologie et apprentissage par le jeu."}
            ],
            "Formations Divers": [
                {"title": "Canva / Illustrator / Photoshop", "price": "6 000 DA", "desc": "Dur�e: 16h / logiciel. Design Graphique."},
                {"title": "R � Statistiques / LaTeX / Matlab", "price": "4 000 DA", "desc": "Dur�e: 16h � 24h. Statistiques & Calcul."},
                {"title": "Introduction Photo / Montage Vid�o", "price": "6 000 DA", "desc": "Dur�e: 16h / module. Audiovisuel."}
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
