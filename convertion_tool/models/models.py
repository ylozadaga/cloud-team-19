import enum
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()

CASCADE = 'all, delete, delete-orphan'


class Formats(enum.Enum):
    MP3 = 1,
    ACC = 2,
    AGG = 3,
    WAV = 4,
    WMA = 5


class Status(enum.Enum):
    UPLOADED = 1,
    PROCESSING = 2,
    PROCESSED = 3


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Enum(Status))
    input_format = db.Column(db.Enum(Status))
    output_format = db.Column(db.Enum(Status))
    timestamp = db.Column(db.TIMESTAMP)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    email = db.Column(db.String(50))
    tasks = db.relationship('Task', cascade=CASCADE)


class FormatsToDic(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return {'format': value.name, 'id': value.value}


class StatusToDic(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return {'status': value.name, 'id': value.value}


class TaskSchema(SQLAlchemyAutoSchema):
    status = StatusToDic(attribute='status')
    input_format = FormatsToDic(attribute='input_format')
    output_format = FormatsToDic(attribute='output_format')

    class Meta:
        model = Task
        include_relationships = True
        include_fk = True
        load_instance = True

    timestamp = fields.String()


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = True
        load_instance = True

    tasks = fields.Nested(TaskSchema())

