from flask import Blueprint, jsonify, request, current_app
from app.auth import token_required

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
    user = request.get_json()
    if not user:
        return {
            "message": "Please provide user details",
            "data": None,
            "error": "Bad request"
        }, 400
    
    # TODO: Validate the user details
    
    # Add the user to the database
    current_app.db.insertUser(user['email'], user['password'], user['name'])
    return {
        "message": "User registered successfully",
        "data": user,
        "error": None
    }, 201


@routes.route('/login', methods=['POST'])
def login():
     try:
        user = request.json
        if not user:
            return {
                "message": "Please provide user details",
                "data": None,
                "error": "Bad request"
            }, 400
        
        email = user.get('email')
        password = user.get('password')

        if not email or not password:
            return {
                "message": "Please provide email and password",
                "data": None,
                "error": "Bad request"
            }, 400
        
        # Make a query to the database to check if the user exists

        # Next, check if the password is correct

        #

        return {
            "message": "User logged in successfully",
            "data": user,
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
    user = request.json
    if not event_id:
        return {
            "message": "Please provide event id",
            "data": None,
            "error": "Bad request"
        }, 400
    
    if not user:
        return {
            "message": "Please provide user details",
            "data": None,
            "error": "Bad request"
        }, 400
    
    email = user.get('email')
    if not email:
        return {
            "message": "Please provide email",
            "data": None,
            "error": "Bad request"
        }, 400
    
    # Make a query to the database to check if the user already exists

    # Next, save the user to the database

    return {
        "message": "User registered for event successfully",
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