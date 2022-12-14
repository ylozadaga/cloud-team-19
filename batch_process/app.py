from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from models import db, User, UserSchema, Task, TaskSchema, File, Formats, Status
from views import PingPongView
from google.oauth2 import service_account
from werkzeug.utils import secure_filename
import google.cloud.storage as storage
import google.cloud.pubsub as pubsub
import os
import subprocess
import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://root:admin123@10.54.241.3:5432/convertion-tool'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = 'testseguridadarqui@gmail.com'
app.config['MAIL_PASSWORD'] = 'mjeqqyxihistrnue'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app_context = app.app_context()
app_context.push()

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

with app_context:
    cors = CORS(app)
    api = Api(app)
    api.add_resource(PingPongView, '/api/ping')

    subscriber = pubsub.SubscriberClient().from_service_account_file('convertion-tool.json')
    subscription_path = 'projects/convertion-tool/subscriptions/new-convertion-task-sub'


    def convert_file(input_file_name, output_file_name, output_format):
        print('comienza el job')
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

        print('termina y envia el mensaje')
        '''send_message(mail, user.email, input_path.split("/")[-1], output_format)'''


def callback(message):
    print(f'mensaje recibido: {message}')
    print(f'data: {message.data}')
    input_file_name = message.attributes.get('input_file_name')
    output_file_name = message.attributes.get('output_file_name')
    output_format = message.attributes.get('output_format')
    convert_file(input_file_name, output_file_name, output_format)
    message.ack()


streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f'escuchando los mensajes del topico {subscription_path}')

with subscriber:
    try:
        streaming_pull_future.result()
    except TimeoutError:
        streaming_pull_future.cancel()
        streaming_pull_future.result()
