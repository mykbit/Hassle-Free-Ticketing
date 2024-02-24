from flask import Blueprint, jsonify, request, current_app
from app import utils

routes = Blueprint('routes', __name__)

@routes.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "Welcome to the API",
        "data": None,
        "error": None
    }), 200

@routes.route('/register', methods=['POST'])
def register():
    print("Hello")
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
    
    # Make a query to the database to check if the user already exists

    # Next, save the user to the database

    return {
        "message": "User registered successfully",
        "data": user,
        "error": None
    }, 201


