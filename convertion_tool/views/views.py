from flask_jwt_extended import jwt_required, create_access_token
from flask_restful import Resource


class SignUpView(Resource):
    def post(self):
        return None


class LogInView(Resource):
    def post(self):
        return None


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

