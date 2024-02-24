from flask import Flask

from .models import connect_db
from .tables import create_tables
from .config import Config

# Function to create and configure the Flask app
def create_app():
    # Initialize Flask app
    app = Flask(__name__)

    # Load configuration from config.py
    app.config.from_object(Config)

    # Create tables in the database
    with app.app_context():
        create_tables()

    # Initialize database connection
    with app.app_context():
        db_connection = connect_db()

    # Add the database connection to the Flask app context
    app.db = db_connection

    # Import routes after initializing app to avoid circular imports
    from .routes import routes

    # Register routes with the Flask app. You can set a different prefix for all routes as well as the home route.
    app.register_blueprint(routes, url_prefix='/')

    return app