from flask import Blueprint, render_template, request
from database import get_db
from filters import filter_explicit_content
import sqlite3

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    return render_template('index.html')

@bp.route('/search')
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
            title = row['title']
            url = row['url']
            description = row['description']
            query_lower = query.lower()
            description_lower = description.lower()

            # Trouver la position de la requête dans la description
            pos = description_lower.find(query_lower)

            if pos != -1:
                # Extraire les mots autour de la requête
                words = description.split()
                # Trouver l'index du mot où commence la requête
                query_word_index = -1
                for i, word in enumerate(words):
                    if query_lower in word.lower():
                        query_word_index = i
                        break

                if query_word_index != -1:
                    # Extraire les 10 mots avant et les 20 mots après
                    start_index = max(0, query_word_index - 10)
                    end_index = min(len(words), query_word_index + 21)
                    snippet_words = words[start_index:end_index]
                    snippet_final = ' '.join(snippet_words)
                else:
                    snippet_final = description[:100] + '...'
            else:
                snippet_final = description[:100] + '...'

            results.append({
                'title': title,
                'href': url,
                'body': snippet_final
            })

        # Suppression des doublons
        unique_results = []
        seen_titles = set()
        for result in results:
            if result['title'] not in seen_titles:
                unique_results.append(result)
                seen_titles.add(result['title'])
        results = unique_results

        # Application du filtre
        results = filter_explicit_content(results)
        if not results:
            error_message = "Aucun résultat trouvé pour votre recherche"

    except sqlite3.Error as e:
        print(f"Erreur lors de la recherche dans la base de données: {e}")
        error_message = "Une erreur s'est produite lors de la recherche. Veuillez réessayer plus tard."

    finally:
        db.close()


    return render_template('search.html', recherche=recherche, results=results, query=query, error=error_message)@bp.route('/robots.txt')

def robots_txt():
    robots = (
        "User-agent: *\n"
        "Disallow:\n"
    )
    return Response(robots, mimetype='text/plain')
