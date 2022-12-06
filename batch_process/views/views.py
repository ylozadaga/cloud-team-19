from flask_restful import Resource
from models import db, User, UserSchema, Task, TaskSchema, File, Formats, Status
from google.oauth2 import service_account
from werkzeug.utils import secure_filename
import google.cloud.storage as storage
import google.cloud.pubsub as pubsub
import os
import subprocess
import time

project = 'convertion-tool'
bucket_name = 'convertion-tool-storage'
local_path = 'file_storage'
sa_file_name = 'convertion-tool.json'

credentials = service_account.Credentials.from_service_account_file(sa_file_name)
subscriber = pubsub.SubscriberClient.from_service_account_file(sa_file_name)
topic_path = 'projects/convertion-tool/topics/new-convertion-task'

audio_formats = {
    "mp3": '{} "{}" -q:a 0 -map_metadata 0 -id3v2_version 3 "{}"',
    "wav": '{} "{}" -c:a pcm_s16le -f wav "{}"',
    "aac": '{} "{}" -c:a aac -strict experimental "{}"',
    "ogg": '{} "{}" -c:a libvorbis "{}"',
    "wma": '{} "{}" -c:a wmav2 "{}"',
}


class PingPongView(Resource):

    def get(self):
        return "pong", 200


def convert_file(task_id):
    print('comienza el job')
    pending_task = Task.query.get_or_404(task_id)
    if pending_task is not None:
        output_format = pending_task.output_format
        input_file_name = pending_task.file.input_file
        output_file_name = pending_task.file.output_file

        secure_input_file_name = secure_filename(input_file_name)
        input_file_local_path = os.path.join(local_path, secure_input_file_name)

        secure_output_file_name = secure_filename(output_file_name)
        output_file_local_path = os.path.join(local_path, secure_output_file_name)

        client = storage.Client(credentials=credentials, project=project)
        bucket = client.get_bucket(bucket_name)
        blob = bucket.blob(input_file_local_path)
        blob.download_to_filename(input_file_local_path)

        start = time.perf_counter()
        exec_process = audio_formats[output_format.lower()].format("ffmpeg -i", input_file_local_path,
                                                                   output_file_local_path)
        print(exec_process)
        subprocess.call(exec_process, shell=True)
        end = time.perf_counter()
        total_time = end - start
        print(f"Tiempo de conversion: {total_time}")

        client = storage.Client(credentials=credentials, project=project)
        bucket = client.get_bucket(bucket_name)
        blob = bucket.blob(output_file_local_path)
        blob.upload_from_filename(output_file_local_path)

        pending_task.status = Status.PROCESSED
        db.session.commit()
        print('termina y envia el mensaje')
        '''send_message(mail, user.email, input_path.split("/")[-1], output_format)'''
    print('es null')
