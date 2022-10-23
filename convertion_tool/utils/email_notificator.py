from flask_mail import *


def notificar():
    message = Message('Codigo Notificacion Finalizacion Conversion',
                      sender=app.config["MAIL_USERNAME"],
                      recipients=[request.json["correo"]])
    message.body = 'mensaje'
    mail.send(message)
    return True
