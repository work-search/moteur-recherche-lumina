from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import requests
import os
import json
import wikipedia
import threading
import time
from functools import wraps
import sqlite3
from datetime import datetime
import pytz
from bs4 import BeautifulSoup
from functools import wraps
import logging
import re

app = Flask(__name__)
app.secret_key = ''

class SimpleCache:
    def __init__(self):
        self.cache = {}
        self.lock = threading.Lock()

    def get(self, key):
        with self.lock:
            item = self.cache.get(key)
            if item is not None and item[1] > time.time():
                return item[0]
            else:
                return None

    def set(self, key, value, timeout=0):
        with self.lock:
            if timeout > 0:
                self.cache[key] = (value, time.time() + timeout)
            else:
                self.cache[key] = (value, float('inf'))

class AntiDDoS:
    def __init__(self, app=None, max_requests=100, time_window=60, block_time=300):
        self.max_requests = max_requests
        self.time_window = time_window
        self.block_time = block_time
        self.cache = SimpleCache()
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.before_request(self.check_request)

    def check_request(self):
        client_ip = request.remote_addr
        current_time = time.time()

        # Check if IP is blocked
        if self.cache.get(f"blocked:{client_ip}"):
            return "Trop de requêtes. Veuillez réessayer plus tard.", 429

        # Get request history
        requests = self.cache.get(client_ip) or []
        requests = [t for t in requests if current_time - t < self.time_window]

        # Check request count
        if len(requests) >= self.max_requests:
            self.cache.set(f"blocked:{client_ip}", True, timeout=self.block_time)
            return "Trop de requêtes. Veuillez réessayer plus tard.", 429

        # Add new request
        requests.append(current_time)
        self.cache.set(client_ip, requests, timeout=self.time_window)
        return None

anti_ddos = AntiDDoS(app)

# Liste des annonces
announcements = [
    {"title": "api 06/01/2025",
     "content": "Ajout d'une api des articles via des requets. Doc: https://work.weblink.ovh/api/doc/article"},
    {"title": "Extension 27/11/24",
     "content": "Ajout d'une extension firefox pour ajouter work search comme moteur de recherche principaux https://addons.mozilla.org/fr/firefox/addon/work-search/?utm_source=addons.mozilla.org&utm_medium=referral&utm_content=search."},
    {"title": "Filtre 14/11/24",
     "content": "Ajout d'un filtre de recherche explicite + ajout d'un systÃ¨me de log des recherches de tous les utilisateur."},
    {"title": "Ajout de bdd 07/11/24",
     "content": 'Ajout de la recherche dans notre base de donnÃ©es.'},
    {"title": "Bouton pour les rÃ©saux mis en place 03/11/24",
     "content": 'mis en place d\'un bouton qui mene vers les rÃ©saux de "WORK" rapidement.'},
    {"title": "Mise en place d'un acces rapide vers une boite Ã  don 23/10/24",
     "content": 'mis en place d\'un acces rapide vers une boite Ã  don communautaire.'},
    {"title": "mis en place d'un acces rapide au serveur discord 23/10/24",
     "content": 'crÃ©ation d\'un bouton menant au serveur discord communotaire.'},
    {"title": "CrÃ©ation du serveur dicord 23/10/24",
     "content": 'CrÃ©ation d\'un serveur discord communotaire.'},
    {"title": "Ajout du logo 18/10/24",
     "content": 'Ajout du logo du site Ã  cÃ´tÃ© du nom dans l\'onglet.'},
    {"title": "Liens utile 17/10/24",
     "content": 'Ajout de la page "liens utiles".'},
    {"title": "Wikipedia 15/10/24",
     "content": "Ajout de la fonction de faire une recherche sur wikipedia."},
    {"title": "404 11/10/24",
     "content": "Page 404 ajoutÃ©"},
    {"title": "Mise Ã  jour 07/10/24",
     "content": "Mise Ã  jour de la page d'annonce et quelques corrections du site."},
    {"title": "Maintenance 27/09/24",
     "content": "Veuillez noter que notre site sera en maintenance le samedi 27 septembre de 19h Ã  19h10."},
    {"title": "Ajout de la fonction d'annonce 27/09/24",
     "content": "Ajout de la fonctionnalitÃ© d'annonce, toutes les annonces du site y seront affichÃ©es."}
]

def get_db():
    try:
        db = sqlite3.connect('sites_web.db')
        db.row_factory = sqlite3.Row
        return db
    except sqlite3.Error as e:
        print(f"Erreur de connexion Ã  la base de donnÃ©es : {e}")
        return None

users = {
}

@app.route('/')
def home():
    return render_template('search.html')

def filter_explicit_content(results):
    explicit_keywords = ["sexe", "pornographie", "violence", "porno", "pucelle", "porn",
                         "+18", "fuck", "Mia Khalifa", "arme", "gun", "god", "orgasme", "ejaculation", "feu","bombe", "fusil",
                         "cartel", "pistolet", "munition", "couteau", "violence",
                         "violeur","pedophile","sex toys", "absu sexuel", "NuditÃ©",
                         "Ã‰rotique", "Drogue", "Suicide", "Terrorisme", "poki",
                         "crazy game", "pute", "putain", "prostituÃ©", "rencontre", "string",
                         "fesse", "cul", "-18", "organe gÃ©niteur"]
    filtered_results = []
    for result in results:
        if not any(keyword in result['title'].lower() or keyword in result['body'].lower() for keyword in
                   explicit_keywords):
            filtered_results.append(result)
    return filtered_results

@app.route('/search')
def search():
    start_time = time.time()
    query = request.args.get('q', '').strip()
    if not query:
        return render_template('search.html')

    if len(query.split()) == 1:
        definition = get_word_definition(query)
        if definition:
            return render_template('results.html', query=query, definition=definition)

    recherche = query
    error_message = None
    results = []

    db = get_db()
    if db is None:
        error_message = "Erreur de connexion Ã  la base de donnÃ©es"
        return render_template('results.html', recherche=recherche, results=[], query=query, error=error_message)

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

        if session.get('safe_search', True):
            results = filter_explicit_content(results)

        if not results:
            error_message = "Aucun rÃ©sultat trouvÃ© pour votre recherche"

    except sqlite3.Error as e:
        print(f"Erreur lors de la recherche dans la base de donnÃ©es: {e}")
        error_message = "Une erreur s'est produite lors de la recherche. Veuillez rÃ©essayer plus tard."
    finally:
        db.close()

    paris_tz = pytz.timezone('Europe/Paris')
    current_date_and_time = datetime.now(paris_tz)
    with open('log.txt', 'a') as f:
        f.write(f"nouvelle recherche: {query} Ã  {current_date_and_time.strftime('%Y-%m-%d %H:%M:%S %Z')}\n")

    end_time = time.time()
    search_time = round(end_time - start_time, 2)

    return render_template('results.html', recherche=recherche, results=results, query=query, search_time=search_time,
                           error=error_message)

def get_word_definition(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/fr/{word}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data and isinstance(data, list) and len(data) > 0:
                meanings = data[0].get('meanings', [])
                if meanings:
                    return meanings[0].get('definitions', [{}])[0].get('definition', '')
    except requests.RequestException:
        pass
    return None

@app.route('/announcements')
def show_announcements():
    return render_template('announcement.html', announcements=announcements)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/wiki_search')
def wiki_search():
    query = request.args.get('q')
    try:
        wikipedia.set_lang("fr")
        page = wikipedia.page(query)
        result = {
            'title': page.title,
            'url': page.url,
            'summary': page.summary
        }
    except wikipedia.exceptions.DisambiguationError as e:
        result = {
            'title': "Plusieurs rÃ©sultats possibles",
            'url': '',
            'summary': str(e.options)
        }
    except wikipedia.exceptions.PageError:
        result = {
            'title': "Pas de rÃ©sultat",
            'url': '',
            'summary': "Aucune page Wikipedia trouvÃ©e pour cette recherche."
        }
    return render_template('wiki_result.html', result=result, query=query)

@app.route('/liens_utiles')
def liens_utiles():
    useful_links = [
        {
            "title": "Le Robert en ligne",
            "url": "https://dictionnaire.lerobert.com/",
            "description": "Outils de dictionaire en ligne"
        },
        {
            "title": "WikipÃ©dia",
            "url": "https://fr.wikipedia.org/wiki/Wikip%C3%A9dia:Accueil_principal",
            "description": "encyclopÃ©die en ligne."
        },
        {
            "title": "ecole direct",
            "url": "https://www.ecoledirecte.com/",
            "description": "Espace de travail Scolaire"
        },
        {
            "title": "ecole direct plus",
            "url": "https://ecole-directe.plus/login",
            "description": "Une version non-officiel amÃ©liorÃ© de Ecole direct avec des fonction en plus"
        },
        {
            "title": "deepl",
            "url": "https://www.deepl.com/fr/translator",
            "description": "traducteur de texte en ligne"
        },
        {
            "title": "lumni",
            "url": "https://www.lumni.fr/",
            "description": "site pour rÃ©viser avec quizz et cour en ligne"
        },
    ]
    return render_template('liens_utiles.html', useful_links=useful_links)

@app.route('/jeu')
def page_jeu():
    return render_template('jeu.html')

@app.route('/db_search')
def db_search():
    query = request.args.get('q', '')
    if not query:
        return render_template('db_search.html', query=query)

    paris_tz = pytz.timezone('Europe/Paris')
    current_date_and_time = datetime.now(paris_tz)
    user_ip = request.remote_addr

    with open('log.txt', 'a') as f:
        f.write(
            f"nouvelle recherche BDD: {query} Ã  {current_date_and_time.strftime('%Y-%m-%d %H:%M:%S %Z')} - IP: {user_ip}\n")

    db = get_db()
    if db is None:
        return render_template('db_search.html', query=query, error="Erreur de connexion Ã  la base de donnÃ©es")

    try:
        cursor = db.cursor()
        cursor.execute("""
            SELECT * FROM articles
            WHERE title LIKE ? OR description LIKE ?
            LIMIT 50
        """, ('%' + query + '%', '%' + query + '%'))

        results = cursor.fetchall()
        return render_template('db_search.html', query=query, results=results)
    except sqlite3.Error as e:
        return render_template('db_search.html', query=query, error=f"Erreur de base de donnÃ©es : {e}")
    finally:
        if db:
            db.close()

@app.route('/api/doc/article')
def doc_api():
    return render_template('doc_api.html')

@app.route('/api/article/<recherche>')
def api_article_search(recherche):
    db = get_db()
    if db is None:
        return jsonify({"error": "Erreur de connexion Ã  la base de donnÃ©es"}), 500

    try:
        cursor = db.cursor()
        cursor.execute("""
            SELECT * FROM articles
            WHERE title LIKE ? OR description LIKE ?
            LIMIT 50
        """, ('%' + recherche + '%', '%' + recherche + '%'))

        results = cursor.fetchall()
        articles = []
        for row in results:
            articles.append({
                "id": row['id'],
                "title": row['title'],
                "description": row['description'],
                "url": row['url']
            })

        return jsonify({"articles": articles})
    except sqlite3.Error as e:
        return jsonify({"error": f"Erreur de base de donnÃ©es : {str(e)}"}), 500
    finally:
        if db:
            db.close()

            
            
            
            
            
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    log_content = read_log_file()
    message_content = read_message_file()
    return render_template('dashboard.html', username=session['username'], log_content=log_content,
                           message_content=message_content)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return "Nom d'utilisateur ou mot de passe incorrect", 401
    return render_template('login.html')

@app.route('/send', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        contact = request.form['contact']
        nom = request.form['nom']
        prenom = request.form['prenom']
        message = request.form['message']

        paris_tz = pytz.timezone('Europe/Paris')
        current_date_and_time = datetime.now(paris_tz)

        with open('message.txt', 'a') as f:
            f.write(
                f"nouveau message:\nDe {prenom} {nom} Ã  {current_date_and_time.strftime('%Y-%m-%d %H:%M:%S %Z')}\n{message}\ncontact: {contact}\n\n")

        return redirect(url_for('home'))

    return render_template('send.html')

def read_log_file():
    log_path = 'log.txt'
    try:
        with open(log_path, 'r') as file:
            return file.read()
    except IOError:
        return "Erreur: Impossible de lire le fichier log.txt"

def read_message_file():
    message_path = 'message.txt'
    try:
        with open(message_path, 'r') as file:
            return file.read()
    except IOError:
        return "Erreur: Impossible de lire le fichier message.txt"

@app.route('/dons')
def dons():
    return render_template('donnateur.html')

@app.route('/extension')
def extension():
    return render_template('extension.html')

@app.route("/robots.txt")
def robots_txt():
    content = """
User-agent: *
Disallow: /login
Disallow: /dashboard
"""
    paris_tz = pytz.timezone('Europe/Paris')
    current_date_and_time = datetime.now(paris_tz)

    with open('log.txt', 'a') as f:
        f.write(f"quelqu'un /quelque chose a accÃ©dÃ© Ã  robots.txt Ã  {current_date_and_time.strftime('%Y-%m-%d %H:%M:%S %Z')}\n")

    return content


@app.route('/.well-known/discord')
def discordergreg():
    return render_template('discord')

@app.route('/faq')
def faq():
    return render_template('faq.html')




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('SERVER_PORT', 5000)))
