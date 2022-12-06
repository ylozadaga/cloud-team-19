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

    @staticmethod
    def from_str(key):
        upper_key = key.upper()
        if upper_key == 'MP3':
            return Formats.MP3
        elif upper_key == 'ACC':
            return Formats.ACC
        elif upper_key == 'AGG':
            return Formats.AGG
        elif upper_key == 'WAV':
            return Formats.WAV
        elif upper_key == 'WMA':
            return Formats.WMA
        else:
            raise NotImplementedError


class Status(enum.Enum):
    UPLOADED = 1,
    PROCESSED = 2


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    input_file = db.Column(db.String)
    output_file = db.Column(db.String)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Enum(Status))
    input_format = db.Column(db.Enum(Formats))
    output_format = db.Column(db.Enum(Formats))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)
    file = db.relationship('File', cascade=CASCADE, uselist=False)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password1 = db.Column(db.String(50))
    password2 = db.Column(db.String(50))
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


class FileSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = File
        include_relationships = True
        include_fk = True
        load_instance = True


class TaskSchema(SQLAlchemyAutoSchema):
    status = StatusToDic(attribute='status')
    input_format = FormatsToDic(attribute='input_format')
    output_format = FormatsToDic(attribute='output_format')

    class Meta:
        model = Task
        include_relationships = True
        include_fk = True
        load_instance = True

    file = fields.Nested(FileSchema())
    created_at = fields.String()
    modified_at = fields.String()


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = True
        load_instance = True

    tasks = fields.Nested(TaskSchema())
