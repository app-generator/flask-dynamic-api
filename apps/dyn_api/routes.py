# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import json

from flask import request
from werkzeug.datastructures import MultiDict

from apps.dyn_api import blueprint
from apps.dyn_api.util import Utils
from flask_restx import Resource
from apps.config import DYNAMIC_API as config


@blueprint.route('/<string:model_name>', methods=['POST', 'GET', 'DELETE', 'PUT'])
@blueprint.route('/<string:model_name>/<int:model_id>', methods=['GET', 'DELETE', 'PUT'])
def dynamic_api(model_name: str, model_id: int = None):
    try:
        manager = Utils.get_manager(config, model_name)
        cls = Utils.get_class(config, model_name)
    except KeyError:
        return {
                   'message': 'this endpoint does not config or not exist!'
               }, 404
    try:
        body_of_req = request.json
    except Exception:
        if len(request.data) > 0:
            body_of_req = json.loads(request.data)
    FormClass = Utils.get_form(config, model_name)
    if request.method == 'POST':
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
    elif request.method == 'GET':
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
    elif request.method == 'DELETE':
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
    elif request.method == 'PUT':
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
