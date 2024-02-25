from functools import wraps
import json
import jwt
from flask import jsonify, request, current_app
from .models import query_db, connect_db, check_token, getClient

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.headers["Authorization"].split(" ")[1]
        current_user = None
        if not token:
            return {
                "message": "Authentication Token is missing!",
                "data": None,
                "error": "Unauthorized"
            }, 401

        match = check_token(token)
        if match != False:
            current_user = getClient(match)
            
            if not current_user:
                return {
                    "message": "User not found",
                    "data": current_user,
                    "error": "Unauthorized"
                }, 401
            
        

        return func(current_user, *args, **kwargs)

    return decorated
