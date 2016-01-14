# -*- coding: utf-8 -*-
import cherrypy
import hashlib, os
from jinja2 import *
from models import User, get_email_mailer, get_passw_mailer

# las bibliotecas que podemos usar
import smtplib
import email.utils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# asignamos los valores para iniciar sesion
try:
    myemail = os.environ["EMAIL_MAILER"]
except Exception, e:
    myemail = get_email_mailer()
try:
    mypassword = os.environ["PASSW_MAILER"]
except Exception, e:
    mypassword = get_passw_mailer()

# método ejemplo de como enviar a un solo correo
def single_email(nombre=None, correo=None, asunto=None, mensaje=None):

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = asunto
    msg['From'] = email.utils.formataddr(("Ruido Vivo", myemail))
    msg['To'] = email.utils.formataddr((nombre, correo))

    # Create the body of the message (a plain-text and an HTML version).
    #text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttps://www.python.org"
    html = create_html(nombre)

    # Record the MIME types of both parts - text/plain and text/html.
    #part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    #msg.attach(part1)
    msg.attach(part2)

    server = smtplib.SMTP("smtp.gmail.com", 587)
    try:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(myemail, mypassword)
        server.sendmail(myemail, [correo], msg.as_string())
        server.quit()
        server.close()
        return True
    except Exception, e:
        print e
        return False

# método ejemplo para crear el cuerpo del mensaje en html
def create_html(usuario):
    return """\
    <html>
        <head></head>
        <body>
            <p>Hi! %s<br>
            How are you?<br>
            Here is the <a href="https://www.python.org">link</a> you wanted.
        </p>
        </body>
    </html>""" %usuario

class MailerController(object):

    @cherrypy.expose
    def test(self):
        if single_email(nombre="yorche", correo="yorche@ciencias.unam.mx", asunto="prueba cherrypy"):
            return "se envio"
        return "no se envio"

cherrypy.tree.mount(MailerController(), "/mailer", "app.conf")