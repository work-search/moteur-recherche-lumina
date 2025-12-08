import sqlite3

def get_db():
    try:
        db = sqlite3.connect('sites_web.db')
        db.row_factory = sqlite3.Row
        return db
    except sqlite3.Error as e:
        print(f"Erreur de connexion à la base de données : {e}")
        return None
