from flask import Blueprint, jsonify, request, current_app
from app.auth import token_required
from app.models import insertClient, insertEvent, getEventDetails, validate_user, session_add, get_contents_clients, get_contents_sessions

from app import utils
import jwt
import time
import sys
import json

routes = Blueprint('routes', __name__)

@routes.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "Welcome to the API",
        "data": None,
        "error": None
    }), 200
    
@routes.route('/table', methods=['GET'])
def view_table():
    return jsonify({
        "message": "Table retrieved successfully",
        "data": get_contents_clients(),
        "error": None
    }), 200

@routes.route('/session', methods=['GET'])
def view_session():
    return jsonify({
        "message": "Session retrieved successfully",
        "data": get_contents_sessions(),
        "error": None
    }), 200

# user fields: email, password, name
@routes.route('/register', methods=['POST'])
def register():
    client = request.get_json()
    if not client:
        return {
            "message": "Please provide client details",
            "data": None,
            "error": "Bad request"
        }, 400
    
    # Add the client to the database
    if insertClient(client['name'], client['email'], client['password']):

        payload  = {'email': client['email']}
        token, expiryDate = session_add(payload['email'])
        return {
            "message": "client registered successfully",
            "data": {
                "token": token,
                "expiryDate": expiryDate
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
        client = request.get_json()
        if not client:
            return {
                "message": "Please provide client details",
                "data": None,
                "error": "Bad request"
            }, 400

        
        # Make a query to the database to check if the client exist

        if validate_user(client['email'], client['password']):

            token, expiryDate = session_add(client['email'])
            return {
                "message": "client logged in successfully",
                "data": {
                    "token": token,
                    "expiration": expiryDate
                },
                "error": None
            }, 200
        
        else:
            return {
                "message": "Invalid email or password",
                "data": None,
                "error": "Unauthorized"
            }, 401
     
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
    
    # insertClient("name", "test", "pass")
    # insertEvent("EventName", event_id, "2024-02-24", "test")

    eventDetails = getEventDetails(event_id)

    if eventDetails:
        return {
            "message": "Event retrieved successfully",
            "data": eventDetails,
            "error": None
        }, 200
    else:
        return {
            "message": "Event not found",
            "data": None,
            "error": None
        }, 404
    
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
    statements = utils.filter_payments(statements)
    # FIXME: pass event id
    validate_payment(statements, 'event_id')

    return {
        "message": "File uploaded successfully",
        "data": None,
        "error": None
    }, 200
