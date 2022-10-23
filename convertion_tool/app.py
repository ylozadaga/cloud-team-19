from flask import Flask
from flask_mail import *
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from models import db
from views import PingPongView, SignUpView, LogInView, FileView, TaskView, TasksView

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///convertion-tool.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'frase-secreta'
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = 'testseguridadarqui@gmail.com'
app.config['MAIL_PASSWORD'] = 'mjeqqyxihistrnue'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

cors = CORS(app)
jwt = JWTManager(app)
mail = Mail(app)
api = Api(app)
api.add_resource(PingPongView, '/api/ping')
api.add_resource(SignUpView, '/api/auth/signup')
api.add_resource(LogInView, '/api/auth/login')
api.add_resource(TasksView, '/api/tasks')
api.add_resource(TaskView, '/api/task/<int:id_task>')
api.add_resource(FileView, '/api/files/<filename>')
