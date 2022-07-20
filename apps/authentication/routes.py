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

from apps import db, login_manager
from apps.authentication import blueprint
from apps.authentication.forms import LoginForm, CreateAccountForm
from apps.authentication.models import Users

from apps.authentication.util import verify_pass


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    create_account_form = CreateAccountForm(request.form)
    if 'register' in request.form:

        username = request.form['username']
        email = request.form['email']

        # Check usename exists
        user = Users.query.filter_by(username=username).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Username already registered',
                                   success=False,
                                   form=create_account_form)

        # Check email exists
        user = Users.query.filter_by(email=email).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Email already registered',
                                   success=False,
                                   form=create_account_form)

        # else we can create the user
        user = Users(**request.form)
        db.session.add(user)
        db.session.commit()

        # Delete user from session
        logout_user()

        return render_template('accounts/register.html',
                               msg='User created successfully.',
                               success=True,
                               form=create_account_form)

    else:
        return render_template('accounts/register.html', form=create_account_form)


@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('authentication_blueprint.login'))

@blueprint.route("/login", methods=["POST"])
def login():
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
                user.api_token = jwt.encode(
                    {"user_id": user.id},
                    current_app.config["SECRET_KEY"],
                    algorithm="HS256"
                )
                return {
                    "message": "Successfully fetched auth token",
                    "data": user.api_token
                }
            except Exception as e:
                return {
                           "error": "Something went wrong",
                           "message": str(e)
                       }, 500
        return {
                   'message': 'username or password is wrong',
                   'success': False
               }, 403
    except Exception as e:
        return {
                   "error": "Something went wrong",
                   "message": str(e)
               }, 500
