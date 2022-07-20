# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import jwt
from flask import render_template, redirect, request, url_for, current_app
from flask_login import (
    current_user,
    login_user,
    logout_user
)
from flask_restx import Resource, Api

from apps import db
from apps.authentication import blueprint
from apps.authentication.models import Users

from apps.authentication.util import verify_pass

api = Api(blueprint)
@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('authentication_blueprint.login'))


@api.route('/login', methods=['POST'])
class Login(Resource):
    def post(self):
        try:
            data = request.json
            if not data:
                return {
                           'message': 'username or password is missing',
                           "data": None,
                           'success': False
                       }, 400
            # validate input
            user = Users.query.filter_by(username=data.get('username')).first()
            if user and verify_pass(data.get('password'), user.password):
                try:
                    # token should expire after 24 hrs
                    api_token = jwt.encode(
                        {"user_id": user.id},
                        current_app.config["SECRET_KEY"],
                        algorithm="HS256"
                    )
                    return {
                        "message": "Successfully fetched auth token",
                        "success": True,
                        "data": api_token
                    }
                except Exception as e:
                    return {
                               "error": "Something went wrong",
                               "success": False,
                               "message": str(e)
                           }, 500
            return {
                       'message': 'username or password is wrong',
                       'success': False
                   }, 403
        except Exception as e:
            return {
                       "error": "Something went wrong",
                       "success": False,
                       "message": str(e)
                   }, 500

@api.route('/register', methods=['GET', 'POST'])
class Signup(Resource):
    def post(self):
        try:
            data = request.json
            username = data['username']
            email = data['email']
            user_by_username = Users.query.filter_by(username=username).first()
            if user_by_username:
                return {
                           'message': 'username already exist.',
                           'success': False
                       }, 400
            user_by_email = Users.query.filter_by(email=email).first()
            if user_by_email:
                return {
                           'message': 'email already exist.',
                           'success': False,
                       }, 400
            user = Users(**data)
            db.session.add(user)
            db.session.commit()
            return {
                'message': 'you have signed up.',
                'success': True
            }, 200
        except Exception as e:
            return {
                'message': str(e),
                'success': False,
            }, 500
