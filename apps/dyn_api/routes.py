# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from datetime import datetime

import jwt
from flask import request, current_app
from werkzeug.datastructures import MultiDict
from apps.authentication.models import Users

from apps.authentication.auth_middleware import token_required
from apps.authentication.util import verify_pass
from apps.dyn_api import blueprint
from apps.dyn_api.util import Utils
from flask_restx import Resource, Api
from apps.config import DYNAMIC_API as config
from apps import db

api = Api(blueprint)


@api.route('/<string:model_name>', methods=['POST', 'GET', 'DELETE', 'PUT'])
@api.route('/<string:model_name>/<int:model_id>', methods=['GET', 'DELETE', 'PUT'])
class DynamicAPI(Resource):
    @token_required
    def get(self, model_name: str, model_id: int = None):
        try:
            manager, cls, FormClass = Utils.init_function(config, model_name)
        except KeyError:
            return {
                       'message': 'this endpoint does not config or not exist!'
                   }, 404
        if model_id is None:
            all_objects = manager.all()
            output = [{'id': obj.id, **FormClass(obj=obj).data} for obj in all_objects]
        else:
            obj = manager.get(model_id)
            if obj is None:
                return {
                           'message': 'matching record not found',
                           'success': False
                       }, 404
            output = {'id': obj.id, **FormClass(obj=obj).data}
        return {
                   'data': output,
                   'success': True
               }, 200

    @token_required
    def post(self, model_name: str):
        try:
            manager, cls, FormClass = Utils.init_function(config, model_name)
        except KeyError:
            return {
                       'message': 'this endpoint does not config or not exist!'
                   }, 404
        body_of_req = Utils.standard_request_body(request)
        form = FormClass(MultiDict(body_of_req))
        if form.validate():
            thing = cls(**body_of_req)
            Utils.add_row_to_db(thing, manager)
        else:
            return {
                       'message': form.errors,
                       'success': False
                   }, 400
        return {
                   'message': 'record saved!',
                   'success': True
               }, 200

    @token_required
    def put(self, model_name: str, model_id: int):
        try:
            manager, cls, FormClass = Utils.init_function(config, model_name)
        except KeyError:
            return {
                       'message': 'this endpoint does not config or not exist!'
                   }, 404
        body_of_req = Utils.standard_request_body(request)
        form = FormClass(MultiDict(body_of_req))
        if not form.validate():
            return {
                       'message': form.errors,
                       'success': False
                   }, 404

        to_edit_row = manager.filter_by(id=model_id)

        if to_edit_row is None:
            return {
                       'message': 'matching record not found',
                       'success': False
                   }, 404

        table_cols = [attr.name for attr in to_edit_row.__dict__['_raw_columns'][0].columns._all_columns]
        to_edit_row = to_edit_row.first()
        for col in table_cols:
            value = body_of_req.get(col, None)
            if value:
                setattr(to_edit_row, col, value)
        Utils.commit_changes(manager)
        return {
            'message': 'record updated',
            'success': True
        }

    @token_required
    def delete(self, model_name: str, model_id: int):
        try:
            manager, cls, FormClass = Utils.init_function(config, model_name)
        except KeyError:
            return {
                       'message': 'this endpoint does not config or not exist!'
                   }, 404
        to_delete = manager.filter_by(id=model_id)
        if to_delete.count() == 0:
            return {
                       'message': 'matching record not found',
                       'success': False
                   }, 404
        Utils.remove_rows_from_db(to_delete, manager)
        return {
                   'message': 'record deleted!',
                   'success': True
               }, 200



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
                    return {
                        "message": "Successfully fetched auth token",
                        "success": True,
                        "data": user.api_token
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

@api.route('/register', methods=['POST'])
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
            now = int(datetime.utcnow().timestamp())
            api_token = jwt.encode(
                {"user_id": user.id,
                 "init_date": now},
                current_app.config["SECRET_KEY"],
                algorithm="HS256"
            )
            user.api_token = api_token
            user.api_token_ts = now
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
