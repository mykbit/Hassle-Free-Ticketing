from flask import Blueprint, jsonify, request, current_app
from app.auth import token_required
from app.models import insertClient
from app import utils
import jwt
import time
import sys

routes = Blueprint('routes', __name__)

@routes.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "Welcome to the API",
        "data": None,
        "error": None
    }), 200

# @routes.route('/table', methods=['GET'])
# def view_table_contents():
    
# user fields: email, password, name, revTag="", eventID=""
@routes.route('/register', methods=['POST'])
def register():
    client = request.get_json()
    if not client:
        return {
            "message": "Please provide client details",
            "data": None,
            "error": "Bad request"
        }, 400
    
    # TODO: Validate the client details

    # Add the client to the database
    if insertClient(client['email'], client['password'], client['name']):

        payload  = {'email': client['email']}
        token = jwt.encode(payload, str(current_app.config['JWT_SECRET_KEY']), algorithm="HS256")
        return {
            "message": "client registered successfully",
            "data": {
                "token": token,
                "expiration": int(time.time() + (24 * 60 * 60))
            },
            "error": None
        }, 201
    else:
        return {
            "message": "An error occurred",
            "data": None,
            "error": "Internal server error"
        }, 500

@routes.route('/login', methods=['POST'])
def login():
     try:
        client = request.json
        if not client:
            return {
                "message": "Please provide client details",
                "data": None,
                "error": "Bad request"
            }, 400
        
        email = client.get('email')
        password = client.get('password')

        if not email or not password:
            return {
                "message": "Please provide email and password",
                "data": None,
                "error": "Bad request"
            }, 400
        
        # Make a query to the database to check if the client exists


        # Next, check if the password is correct

        #

        return {
            "message": "client logged in successfully",
            "data": client,
            "error": None
        }, 200
     
     except Exception as e:
        return {
            "message": "An error occurred",
            "data": None,
            "error": str(e)
        }, 500
     
@routes.route('/event/<int:event_id>', methods=['GET'])
def get_event(event_id):
    event_id = request.view_args['event_id']
    if not event_id:
        return {
            "message": "Please provide event id",
            "data": None,
            "error": "Bad request"
        }, 400
    
    # Make a query to the database to get the event details

    return {
        "message": "Event retrieved successfully",
        "data": None,
        "error": None
    }, 200

@routes.route('/event/<int:event_id>/register', methods=['POST'])
def register_for_event(event_id):
    event_id = request.view_args['event_id']
    client = request.json
    if not event_id:
        return {
            "message": "Please provide event id",
            "data": None,
            "error": "Bad request"
        }, 400
    
    if not client:
        return {
            "message": "Please provide client details",
            "data": None,
            "error": "Bad request"
        }, 400
    

    email = client.get('email')
    if not email:
        return {
            "message": "Please provide email",
            "data": None,
            "error": "Bad request"
        }, 400

    # Make a query to the database to check if the client already exists

    # Next, save the client to the database
    return {
        "message": "client registered for event successfully",
        "data": None,
        "error": None
    }, 201

@routes.route('/user', methods=['GET'])
@token_required
def get_user(current_user):
    user_data = {
        "email": current_user['user_id'],
        "name": current_user['name'],
        "email": current_user['email']
    }

    return {
        "message": "User retrieved successfully",
        "data": user_data,
        "error": None
    }, 200

@routes.route('/bank-statement', methods=['POST'])
def bank_statement():
    if 'file' not in request.files or request.files['file'].filename == '':
        return {
            "message": "File expected",
            "data": None,
            "error": "Bad request"
        }, 400

    file = request.files['file']

    if file.filename.rsplit('.', 1)[1].lower() != 'csv':
        return {
            "message": "CSV file expected",
            "data": None,
            "error": "Bad request"
        }, 400

    itarable = utils.stream_to_iterable(file.stream)
    header = ["Type","Product","Started Date","Completed Date","Description","Amount","Fee","Currency","State","Balance"]

    if not utils.is_csv_valid(itarable, header):
        return {
            "message": "CSV structure is invalid",
            "data": None,
            "error": "Bad request"
        }, 400

    statements = utils.parse_csv(itarable)

    # statement has these fields: "Type","Product","Started Date","Completed Date","Description","Amount","Fee","Currency","State","Balance"
    print(statements, file=sys.stderr)

    return {
        "message": "File uploaded successfully",
        "data": None,
        "error": None
    }, 200
