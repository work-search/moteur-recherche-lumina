from flask import Flask, render_template, request
import os
import sqlite3
from datetime import datetime
import pytz

app = Flask(__name__)
app.secret_key = 'fdhfjsjlwww254'

def get_db():
    try:
        db = sqlite3.connect('sites_web.db')
        db.row_factory = sqlite3.Row
        return db
    except sqlite3.Error as e:
        print(f"Erreur de connexion à la base de données : {e}")
        return None

def filter_explicit_content(results):
    explicit_keywords = ["sexe", "pornographie", "violence", "porno", "pucelle", "porn",
                         "+18", "fuck", "Mia Khalifa", "arme", "gun", "god", "orgasme", "ejaculation", "feu","bombe", "fusil",
                         "cartel", "pistolet", "munition", "couteau", "violence",
                         "violeur","pedophile","sex toys", "absu sexuel", "Nudité",
                         "Érotique", "Drogue", "Suicide", "Terrorisme", "poki",
                         "crazy game", "pute", "putain", "prostitué", "rencontre", "string",
                         "fesse", "cul", "-18", "organe géniteur"]
    filtered_results = []
    for result in results:
        if not any(keyword in result['title'].lower() or keyword in result['body'].lower() for keyword in
                   explicit_keywords):
            filtered_results.append(result)
    return filtered_results

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search')
def search():
    query = request.args.get('q', '').strip()
    if not query:
        return render_template('search.html', results=[], query='', error=None)

    recherche = query
    error_message = None
    results = []

    db = get_db()
    if db is None:
        error_message = "Erreur de connexion à la base de données"
        return render_template('search.html', recherche=recherche, results=[], query=query, error=error_message)

    try:
        cursor = db.cursor()
        cursor.execute("""
            SELECT titre as title, url, description
            FROM pages
            WHERE titre LIKE ? OR description LIKE ?
            LIMIT 50
        """, (f'%{query}%', f'%{query}%'))

        for row in cursor.fetchall():
            results.append({
                'title': row['title'],
                'href': row['url'],
                'body': row['description']
            })

        # Supprimer les doublons en utilisant un ensemble
        unique_results = []
        seen_titles = set()
        for result in results:
            if result['title'] not in seen_titles:
                unique_results.append(result)
                seen_titles.add(result['title'])

        results = unique_results

        # Appliquer le filtre Safe Search si activé
        results = filter_explicit_content(results)

        if not results:
            error_message = "Aucun résultat trouvé pour votre recherche"

    except sqlite3.Error as e:
        print(f"Erreur lors de la recherche dans la base de données: {e}")
        error_message = "Une erreur s'est produite lors de la recherche. Veuillez réessayer plus tard."
    finally:
        db.close()

    paris_tz = pytz.timezone('Europe/Paris')
    current_date_and_time = datetime.now(paris_tz)
    with open('log.txt', 'a') as f:
        f.write(f"nouvelle recherche: {query} à {current_date_and_time.strftime('%Y-%m-%d %H:%M:%S %Z')}\n")

    return render_template('search.html', recherche=recherche, results=results, query=query, error=error_message)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('SERVER_PORT', 5000)))