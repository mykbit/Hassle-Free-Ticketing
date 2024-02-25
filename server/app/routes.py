from flask import Blueprint, jsonify, request, current_app
from app.auth import token_required
from app.models import insertClient, getEventDetails, getClient, insertTicket, validate_payment, validate_user, session_add, get_contents_clients, get_contents_sessions, create_event_db

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
                    "expiryDate": expiryDate
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
@token_required
def register_for_event(current_user, event_id):
    # Register client for the event
    try:
        insertTicket(event_id, current_user[0], False)
        return jsonify({
            "message": "Client registered for event successfully",
            "data": event_id,
            "error": None
        }), 201
    
    except Exception as e:
        return jsonify({
            "message": "Failed to register client for event",
            "data": None,
            "error": str(e)
        }), 500

@routes.route('/create-event', methods=['POST'])
@token_required
def create_event(current_user):
    event = request.get_json()
    if not event:
        return {
            "message": "Please provide event details",
            "data": None,
            "error": "Bad request"
        }, 400
    
    # Add the event to the database
    event = create_event_db(event['name'], event['price'], event['date'], current_user[0])
    if event:
        return {
            "message": "Event created successfully",
            "data": event[0],
            "error": None
        }, 201
    else:
        return {
            "message": "An error occurred",
            "data": None,
            "error": "Internal server error"
        }, 500
    



@routes.route('/user', methods=['GET'])
@token_required
def get_user(current_user):
    user_data = {
        "email": current_user['email'],
        "name": current_user['name']
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
