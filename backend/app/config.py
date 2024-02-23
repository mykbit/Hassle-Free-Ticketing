import logging

# This is more of a general configuration file for the application, unlike the __init__.py file which is more specific to the Flask app.
class Config:

    # Debugging and development settings
    DEBUG = True

    # Log level configuration
    LOG_LEVEL = logging.DEBUG
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    