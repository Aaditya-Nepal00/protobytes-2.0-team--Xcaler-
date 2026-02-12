from functools import wraps
from flask import jsonify

def handle_errors(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'message': str(e)}), 500
    return decorated_function

def require_permission(permission):
    """Check if user has required permission"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Check permission logic here
            return f(*args, **kwargs)
        return decorated_function
    return decorator
