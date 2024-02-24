import logging
import os

# This is more of a general configuration file for the application, unlike the __init__.py file which is more specific to the Flask app.
class Config:

    # Get the JWT secret key from the environment
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')

    # Debugging and development settings
    DEBUG = True

    # Log level configuration
    LOG_LEVEL = logging.DEBUG
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    