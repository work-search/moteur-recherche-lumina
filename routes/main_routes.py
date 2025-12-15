from flask import Blueprint, render_template, request, Response
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
        # Préparer la requête FTS5 (échapper les caractères spéciaux)
        fts_query = query.replace('"', '""')
        cursor.execute("""
            SELECT p.titre as title, p.url, p.description,
                   snippet(pages_fts, 1, '', '', '...', 30) as snippet
            FROM pages_fts
            JOIN pages p ON pages_fts.rowid = p.rowid
            WHERE pages_fts MATCH ?
            ORDER BY rank
            LIMIT 50
        """, (f'"{fts_query}"',))

        for row in cursor.fetchall():
            title = row['title']
            url = row['url']
            snippet_final = row['snippet'] if row['snippet'] else row['description'][:100] + '...'

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


    return render_template('search.html', recherche=recherche, results=results, query=query, error=error_message)

@bp.route('/robots.txt')
def robots_txt():
    robots = (
        "User-agent: *\n"
        "Disallow:\n"
    )
    return Response(robots, mimetype='text/plain')
