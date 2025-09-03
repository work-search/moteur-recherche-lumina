from flask import Flask
from config import Config
from routes import main_routes, error_routes

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY

# Enregistrement des routes
app.register_blueprint(main_routes.bp)
app.register_blueprint(error_routes.bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(Config.SERVER_PORT))
