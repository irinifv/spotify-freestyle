import os
from flask import Flask
from web_app.routes.home_routes import home_routes
from web_app.routes.search_routes import search_routes
from app.spotify_helpers import SpotifyAPI

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.urandom(64)

    app.register_blueprint(home_routes)
    app.register_blueprint(search_routes)

    # Initialize SpotifyAPI
    spotify_api = SpotifyAPI()
    app.config['SPOTIFY_API'] = spotify_api

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

# from flask import Flask

# from web_app.routes.home_routes import home_routes
# from web_app.routes.search_routes import search_routes

# def create_app():
#     app = Flask(__name__)
#     app.register_blueprint(home_routes)
#     app.register_blueprint(search_routes)

#     return app

# if __name__ == "__main__":
#     my_app = create_app()
#     my_app.run(debug=True)
