from app import create_app, db
import sqlite3
import os

def migrate():
    app = create_app()
    db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
    
    # Handle the fact that the URI might be an absolute path
    if not os.path.exists(db_path):
        db_path = os.path.join(app.root_path, '..', 'instance', 'noblesse.db')
        
    print(f"Applying migration to {db_path}...")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Add columns if they don't exist
    try:
        cursor.execute("ALTER TABLE service ADD COLUMN is_pack BOOLEAN DEFAULT 0 NOT NULL")
        cursor.execute("ALTER TABLE service ADD COLUMN badge_label VARCHAR(50)")
        cursor.execute("ALTER TABLE service ADD COLUMN original_price VARCHAR(50)")
        cursor.execute("ALTER TABLE service ADD COLUMN savings VARCHAR(100)")
        cursor.execute("ALTER TABLE service ADD COLUMN duration VARCHAR(50)")
        cursor.execute("ALTER TABLE service ADD COLUMN included_courses TEXT")
        print("Columns added successfully.")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e).lower():
            print("Columns already exist. Skipping schema alteration.")
        else:
            print(f"Error altering table: {e}")
            
    conn.commit()
    conn.close()
    
    # Now re-seed the data to populate the new fields and packs
    with app.app_context():
        import seed_db
        print("Re-seeding database to include the new packs...")
        seed_db.seed_data()
        print("Migration and seed completed.")

if __name__ == "__main__":
    migrate()
