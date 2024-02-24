from flask import Blueprint, jsonify
from app import utils, models

routes = Blueprint('routes', __name__)

# Demo Application
@routes.route('/')
def index():
    try:
        models.insert("Sample Event", "2024-02-23", "sample_payment_address")
        return 'Insertion successful!'
    except Exception as e:
        return f'Error during insertion: {str(e)}'
    	
    return 'Hello World'

