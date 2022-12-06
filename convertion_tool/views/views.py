from flask import request
from models import db, User, UserSchema, Task, TaskSchema, File, Formats, Status
from utils.system_utils import delete_file_if_exist
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from flask_restful import Resource
from datetime import datetime
from google.oauth2 import service_account
from werkzeug.utils import secure_filename
import sqlalchemy
import google.cloud.storage as storage
import google.cloud.pubsub as pubsub
import os

project = 'convertion-tool'
bucket_name = 'convertion-tool-storage'
local_path = 'file_storage'
sa_file_name = 'convertion-tool.json'

credentials = service_account.Credentials.from_service_account_file(sa_file_name)
publisher = pubsub.PublisherClient.from_service_account_file(sa_file_name)
topic_path = 'projects/convertion-tool/topics/new-convertion-task'

user_schema = UserSchema()
task_schema = TaskSchema()


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
        file_local_path = os.path.join(local_path, secure_file_name)
        file.save(file_local_path)

        client = storage.Client(credentials=credentials, project=project)
        bucket = client.get_bucket(bucket_name)
        blob = bucket.blob(complete_file_name)
        blob.upload_from_filename(file_local_path)

        input_file_name = file_name + "." + input_format.name.lower()
        output_file_name = (file_name.split(".")[0]) + "." + output_format.name.lower()

        file = File(input_file=input_file_name, output_file=output_file_name)

        task = Task(status=status,
                    input_format=input_format,
                    output_format=output_format,
                    created_at=timestamp,
                    modified_at=timestamp,
                    user_id=user_id,
                    file=file)

        db.session.add(task)
        db.session.add(file)
        db.session.commit()
        delete_file_if_exist(file_local_path)
        attributes = {
            'input_file_name': str(input_file_name),
            'output_file_name': str(output_file_name),
            'new_format': output_format.name.lower()
        }
        future = publisher.publish(topic_path, str(task.id).encode('utf8'), **attributes)
        print(future.result())
        return "Tarea creada correctamente con id: {}".format(task.id), 201


class TaskView(Resource):

    @jwt_required()
    def get(self, id_task):
        return task_schema.dump(Task.query.get_or_404(id_task))

    @jwt_required()
    def post(self, id_task):
        return "Not implemented Method", 501

    @jwt_required()
    def put(self, task_id):
        task = Task.query.get_or_404(task_id)
        new_format_enum = Formats.from_str(request.json['newFormat'])
        if new_format_enum.name is not task.output_format.name:
            task.output_format = new_format_enum
            if Status.PROCESSED.name is task.status.name:
                file = File.query.get_or_404(task.file.id)
                client = storage.Client(credentials=credentials, project=project)
                bucket = client.get_bucket(bucket_name)
                blob = bucket.blob(file.output_file)
                blob.delete()
                file.output_file = file.output_file.split(".")[0] + "." + task.output_format.name.lower()
                task.status = Status.UPLOADED
            task.modified_at = datetime.now()
            db.session.commit()
        return task_schema.dump(task)

    @jwt_required()
    def delete(self, task_id):
        return_message = {"message": "Error during task delete"}
        try:
            task = Task.query.get_or_404(task_id)
            client = storage.Client(credentials=credentials, project=project)
            bucket = client.get_bucket(bucket_name)
            blob_input = bucket.blob(task.file.input_file)
            blob_input.delete()
            if task.status == Status.PROCESSED:
                blob_output = bucket.blob(task.file.output_file)
                blob_output.delete()
                task.file.input_file = sqlalchemy.sql.null()
                task.file.output_file = sqlalchemy.sql.null()
                task.modified_at = datetime.now()
                db.session.commit()
                return_message = {"id_task": task.id,
                                  "status": str(task.status),
                                  "message": "Task input and output files deleted successfully"}

            elif task.status == Status.UPLOADED:
                task.file.input_file = sqlalchemy.sql.null()
                task.file.output_file = sqlalchemy.sql.null()
                task.modified_at = datetime.now()
                db.session.commit()
                return_message = {"id_task": task.id,
                                  "status": str(task.status),
                                  "message": "Task input file deleted successfully"}
            return return_message
        except:
            return return_message


class TaskViewUser(Resource):

    @jwt_required()
    def get(self, id_user):
        return [task_schema.dump(task) for task in User.query.get_or_404(id_user).tasks]


class FileView(Resource):
    @jwt_required()
    def get(self):
        return "Not implemented Method", 501

    @jwt_required()
    def post(self):
        return "Not implemented Method", 501

    @jwt_required()
    def put(self):
        return "Not implemented Method", 501

    @jwt_required()
    def delete(self):
        return "Not implemented Method", 501
