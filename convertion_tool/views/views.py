from flask import request
from models import db, User, UserSchema, Task, TaskSchema, File, FileSchema, Formats, Status
from utils.system_utils import delete_file_if_exist
from flask_jwt_extended import jwt_required, create_access_token
from flask_restful import Resource 

user_schema = UserSchema()
task_schema = TaskSchema()


class PingPongView(Resource):
    def get(self):
        return "pong", 200


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
    def post(self):

        return 'task successfully created with id: ' + id, 201


class TaskView(Resource):

    @jwt_required()
    def get(self, id_task):
        return None

    @jwt_required()
    def post(self, id_task):
        return None

    @jwt_required()
    def put(self, id_task):
        task = Task.query.get_or_404(id_task)
        new_format_enum = Formats.from_str(request.json.get['newFormat'])
        if new_format_enum != task.output_format:
            task.output_format = new_format_enum
            if Status.PROCESSED == task.status:
                file = File.query.get_or_404(task.id_file)
                delete_file_if_exist(file.output_path)
            task.status = Status.UPLOADED
        return None

    @jwt_required()
    def delete(self, id_task):
        return None


class TaskViewUser(Resource):

    @jwt_required()
    def post(self, id_user):
        return None
