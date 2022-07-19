import inspect
import sys

from apps import db
from apps.config import REGISTER_MODEL_MODULE


from wtforms import Form
from wtforms_alchemy import model_form_factory
ModelForm = model_form_factory(Form)

class Utils:
    @staticmethod
    def add_row_to_db(obj, manager: db.Query):
        manager.session.add(obj)
        manager.session.commit()

    @staticmethod
    def remove_rows_from_db(rows, manager: db.Query):
        rows.delete()
        manager.session.commit()

    @staticmethod
    def commit_changes(manager: db.Query):
        db.session.commit()

    @staticmethod
    def get_class(config, name: str) -> db.Model:
        return Utils.model_name_to_class(config[name])

    @staticmethod
    def get_manager(config, name: str) -> db.Query:
        return Utils.get_class(config, name).query

    @staticmethod
    def get_form(config, name: str) -> ModelForm:
        class ThisClassForm(ModelForm):
            class Meta:
                model = Utils.get_class(config, name)

        return ThisClassForm

    @staticmethod
    def model_name_to_class(name: str):
        all_classes = inspect.getmembers(sys.modules[REGISTER_MODEL_MODULE], inspect.isclass)
        for cls in all_classes:
            if cls[0] == name:
                return cls[1]
        # we are confident that never returns None
        return None
