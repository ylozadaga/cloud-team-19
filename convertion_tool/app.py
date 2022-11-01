from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from models import db, User
from views import PingPongView, SignUpView, LogInView, FileView, TaskView, TasksView, TaskViewUser

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://root:admin123@172.17.0.2:5432/convertion-tool'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'frase-secreta'
app.config['PROPAGATE_EXCEPTIONS'] = True
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

cors = CORS(app)
jwt = JWTManager(app)
api = Api(app)
api.add_resource(PingPongView, '/api/ping')
api.add_resource(SignUpView, '/api/auth/signup')
api.add_resource(LogInView, '/api/auth/login')
api.add_resource(TasksView, '/api/tasks')
api.add_resource(TaskView, '/api/task/<int:task_id>')
api.add_resource(FileView, '/api/files/<filename>')
api.add_resource(TaskViewUser, '/api/task/<int:id_user>/user')

with app_context:
    numberUsers = db.session.query(User).count()
    if numberUsers == 0:
        new_user = User(
            username="user01",
            email="userprueba@gmail.com",
            password1="user01",
            password2="user01"
        )
        db.session.add(new_user)
        db.session.commit()
