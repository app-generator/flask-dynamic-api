# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask import request
from werkzeug.datastructures import MultiDict

from apps.authentication.auth_middleware import token_required
from apps.dyn_api import blueprint
from apps.dyn_api.util import Utils
from flask_restx import Resource, Api
from apps.config import DYNAMIC_API as config

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
