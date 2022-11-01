from celery import Celery
from pydub import AudioSegment
from models import User, Task, Status
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine('postgresql://root:admin123@172.17.0.2:5432/convertion-tool')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()




app = Celery('tasks', broker='redis://localhost:6379/0')

Base.metadata.create_all(engine)

session = Session()

'''
app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = 'testseguridadarqui@gmail.com'
app.config['MAIL_PASSWORD'] = 'mjeqqyxihistrnue'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

def send_message(mail, email, input_file_name, output_format):
    message = Message('Notificacion finalizacion de conversion del archivo {}'.format(input_file_name),
                      sender='testseguridadarqui@gmail.com',
                      recipients=email)
    message.body = 'El archivo {} ha sido convertido correctamente al formato {}'.format(input_file_name, output_format)
    mail.send(message)
    return True
'''

@app.task
def convert_file(mail):
    print('comienza el job')
    pending_task = User.query.filter(Task.status == Status.UPLOADED).first()
    if pending_task is not None:
        print('no es null')
        user = User.query.filter(User.id == pending_task.user_id).first()
        input_format = pending_task.input_format
        print('el input format ' + input_format)
        output_format = pending_task.output_format
        print('el output format ' + output_format)
        input_path = pending_task.file.input_path
        print('el input path ' + input_path)
        output_path = pending_task.file.output_path
        print('el output path ' + output_path)
        AudioSegment.from_file(input_path, format=input_format).export(output_path, format=output_format)
        pending_task.status = Status.PROCESSED
        session.commit()
        send_message(mail, user.email, input_path.split("/")[-1], output_format)
    print('es null')
