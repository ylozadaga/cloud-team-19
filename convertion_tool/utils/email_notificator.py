from flask_mail import *
from ..app import app, mail


def notificar(email):
    message = Message('Notificacion finalizacion de conversion de archivos',
                      sender=app.config["MAIL_USERNAME"],
                      recipients=email)
    message.body = 'mensaje'
    mail.send(message)
    return True
