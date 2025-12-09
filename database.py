import sqlite3
import os

def get_db():
    try:
        # Utiliser le chemin absolu pour la base de données
        db_path = os.path.join(os.path.dirname(__file__), 'database', 'sites_web.db')
        db = sqlite3.connect(db_path)
        db.row_factory = sqlite3.Row
        return db
    except sqlite3.Error as e:
        print(f"Erreur de connexion à la base de données : {e}")
        return None
