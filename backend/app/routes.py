from flask import Blueprint, jsonify
from app import utils, models

routes = Blueprint('routes', __name__)

# Demo Application
@routes.route('/')
def index():
    # try:
    #     models.insertEvent("123", "123", "sample_payment_address", "organiser123", "100", "100")

    #     return 'Insertion successful!'
    # except Exception as e:
    #     return f'Error during insertion: {str(e)}'
    	
    return 'Hello World'

@routes.route('/hello')
def hellowRoutes():
    return "This is another page"

