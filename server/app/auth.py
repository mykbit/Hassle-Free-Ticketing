from functools import wraps
import jwt
from flask import request, abort
from flask import current_app
from app.models import models

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return {
                "message": "Authentication Token is missing!",
                "data": None,
                "error": "Unauthorized"
            }, 401
        try:
            data = jwt.decode(token, current_app.config['JWT_SECRET_KEY'])
            current_user = models.query_db(current_app.db_connection, "SELECT * FROM Clients WHERE email=?",
                                            (data['email']))
            if not current_user:
                return {
                    "message": "User not found",
                    "data": None,
                    "error": "Unauthorized"
                }, 401
        except Exception as e:
            return {
                "message": "Something went wrong",
                "data": None,
                "error": "Unauthorized"
            }, 500
        
        return func(current_user, *args, **kwargs)
    
    return decorated
        