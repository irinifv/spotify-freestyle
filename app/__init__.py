from flask import Flask
from web_app.routes.home_routes import home_routes
# from web_app.routes.search_routes import search_routes

def create_app():
    # Initialize Flask app
    app = Flask(__name__, template_folder="../web_app/templates")
    
    # Register blueprints
    app.register_blueprint(home_routes)
    # app.register_blueprint(search_routes)
    
    return app