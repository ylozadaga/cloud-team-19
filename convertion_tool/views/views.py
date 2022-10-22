from flask import request #
from models import db, User, UserSchema #
from flask_jwt_extended import jwt_required, create_access_token
from flask_restful import Resource 
#convertion_tool.models

user_schema = UserSchema()

class SignUpView(Resource):
    def post(self):
        new_user = User(username=request.json["username"], password=request.json["password"], email=request.json["email"])
        db.session.add(new_user)
        db.session.commit()
        return {"mensaje":"cuenta creada exitosamente"}


class LogInView(Resource):
    def post(self):
        new_user = User(username=request.json["username"], password=request.json["password"])
        token_de_acceso = create_access_token(identity = request.json["username"])
        db.session.add(new_user)
        db.session.commit()
        return {"token de acceso":token_de_acceso}


class FileView(Resource):
    @jwt_required()
    def get(self):
        return None

    @jwt_required()
    def post(self):
        return None

    @jwt_required()
    def put(self):
        return None

    @jwt_required()
    def delete(self):
        return None


class TasksView(Resource):

    @jwt_required()
    def get(self):
        return None

    @jwt_required()
    def post(self):
        return None

    @jwt_required()
    def put(self):
        return None

    @jwt_required()
    def delete(self):
        return None


class TaskView(Resource):

    @jwt_required()
    def get(self, id_task):
        return None

    @jwt_required()
    def post(self, id_task):
        return None

    @jwt_required()
    def put(self, id_task):
        return None

    @jwt_required()
    def delete(self, id_task):
        return None


class TaskViewUser(Resource):

    @jwt_required()
    def post(self, id_user):
        return None
