from functools import wraps
import jwt
from flask import request
from flask import current_app
from .models import Users


def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split()[1]
        else:
            return {
                       'message': 'Token is missing',
                       'data': None,
                       'success': False
                   }, 403
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = Users.query.filter_by(id=data['user_id']).first()
            if current_user is None:
                return {
                           'message': 'Invalid token',
                           'data': None,
                           'success': False
                       }, 403
        except Exception as e:
            return {
                'message': str(e),
                'data': None,
                'success': False
            }, 500
        return func(*args, **kwargs)
    return decorated
