from flask import request
from models import db, User, UserSchema, Task, TaskSchema, File, FileSchema, Formats, Status
from utils.system_utils import delete_file_if_exist
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from flask_restful import Resource
from datetime import datetime
from werkzeug.utils import secure_filename
import os

user_schema = UserSchema()
task_schema = TaskSchema()
base_input_path = '/app/file_storage/input/'
base_output_path = '/app/file_storage/output/'


class PingPongView(Resource):
    def get(self):
        return "pong", 200


class SignUpView(Resource):
    def post(self):
        new_user = User(
            username=request.json["username"],
            password1=request.json["password1"],
            password2=request.json["password2"],
            email=request.json["email"])

        if new_user.password1 == new_user.password2:
            if len(new_user.password1)<5:
                return {"mensaje": "La contraseña debe tener más de 5 caracteres"}
            else:
                db.session.add(new_user)
                db.session.commit()
            return {"mensaje": "cuenta creada exitosamente", "id": new_user.id}
        else:
            return {"mensaje": "Las contraseñas no coinciden", "id": new_user.id}


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

    @jwt_required()
    def post(self):
        file = request.files["file"]
        complete_file_name = file.filename
        file_name = complete_file_name.split(".")[0]
        input_format = Formats.from_str(complete_file_name.split(".")[-1])
        output_format = Formats.from_str(request.form.get('newFormat'))
        status = Status.UPLOADED
        timestamp = datetime.now()
        user_id = get_jwt_identity()

        secure_file_name = secure_filename(complete_file_name)
        file.save(os.path.join(base_input_path, secure_file_name))

        file = File(input_path=base_input_path + file_name + "."+input_format.name.lower(),
                    output_path=base_output_path + (file_name.split(".")[0]) + "."+output_format.name.lower())

        task = Task(status=status,
                    input_format=input_format,
                    output_format=output_format,
                    timestamp=timestamp,
                    user_id=user_id,
                    file=file)

        db.session.add(task)
        db.session.add(file)
        db.session.commit()
        
        return "Tarea creada correctamente con id: {}".format(task.id), 201


class TaskView(Resource):

    #@jwt_required()
    def get(self, id_task):
        task = Task.query.get_or_404(id_task)
        return task_schema.dump(task)

    @jwt_required()
    def post(self, id_task):
        return None

    @jwt_required()
    def put(self, task_id):
        task = Task.query.get_or_404(task_id)
        new_format_enum = Formats.from_str(request.json['newFormat'])
        if new_format_enum.name is not task.output_format.name:
            task.output_format = new_format_enum
            if Status.PROCESSED.name is task.status.name:
                file = File.query.get_or_404(task.file.id)
                delete_file_if_exist(file.output_path)
                file.output_path = file.output_path.split(".")[0] + "." + task.output_format.name.lower()
            task.status = Status.UPLOADED
            db.session.commit()
        return task_schema.dump(task)

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
