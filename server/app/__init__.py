from flask import Flask

from .models import init_db
from .config import Config

# Function to create and configure the Flask app
def create_app():
    # Initialize Flask app
    app = Flask(__name__)

    # Load configuration from config.py
    app.config.from_object(Config)

    # Initialize database connection
    with app.app_context():
        db_connection = init_db()

    # Add the database connection to the Flask app context
    app.db_connection = db_connection

    # Import routes after initializing app to avoid circular imports
    from .routes import routes

    # Register routes with the Flask app. You can set a different prefix for all routes as well as the home route.
    app.register_blueprint(routes, url_prefix='/')

    return app