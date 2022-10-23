from flask import request
from sqlite3 import Timestamp
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
        new_user = User(username=request.json["username"],password1=request.json["password1"],
                    password2=request.json["password2"], email=request.json["email"])

        if new_user.password1 == new_user.password2:
            if len(new_user.password1)<5:
                return {"mensaje": "La contraseña debe tener más de 5 caracteres"}
            else:
                db.session.add(new_user)
                db.session.commit()
            return {"mensaje":"cuenta creada exitosamente", "id": new_user.id }
        else:
            return {"mensaje":"Las contraseñas no cohinciden", "id": new_user.id }


class LogInView(Resource):
    def post(self):
        user = User.query.filter(User.username == request.json["username"],
                                User.password1 == request.json["password1"]).first()
        db.session.commit()
        if user is None:
            return "Ese usuario no ha sido registrado", 404
        else:
            token_de_acceso = create_access_token(identity=user.id)
            return {"token": token_de_acceso}


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

    #@jwt_required()
    def post(self):
        args = request.args
        new_task = Task(status = args.get('status'),
                        input_format = args.get('input_format'),
                        output_format = args.get('output_format'),
                        id_user = args.get('id_user'))
        db.session.add(new_task)
        db.session.commit()
        return task_schema.dump(new_task)


class TaskView(Resource):

    #@jwt_required()
    def get(self, id_task):
        task = Task.query.get_or_404(id_task)
        return task_schema.dump(task)

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

    #@jwt_required()
    def get(self, id_user):
        user = User.query.get_or_404(id_user)
        return [task_schema.dump(task) for task in user.tasks]
