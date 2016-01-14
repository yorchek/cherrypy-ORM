# -*- coding: utf-8 -*-
import cherrypy
import hashlib, os, sys
from jinja2 import *
from controllers import *


"""
RuidoVivo developed with CherryPy, SQLAlchemy, Jinja2, Mako, PostgeSQL, SQLite3.
"""

__author__    = 'Yorche Chory'
__contact__   = 'yorchek@gmail.com'
__date__      = 'January 2016'


env = Environment(loader=FileSystemLoader('views'))

class RuidoVivo(object):
    """Controlador de la aplicación Ruido Vivo"""

    @cherrypy.expose
    def index(self):
        try:
            u = cherrypy.session.get(SESSION_KEY)
        except Exception, e:
            u = None
        if u:
            send_to(u)
        #conn = ConPsycopg()
        #conn = ConSQLite()
        #usuarios = conn.consultar("select * from users;")
        html = env.get_template('index.html')
        return html.render(inicioA='active')

    @cherrypy.expose
    def now_playing(self):
        conn = ConPsycopg()
        #conn = ConSQLite()
        cadena = "Usuarios registrados<br>"
        users = conn.consultar("select * from users;")
        if users:
            for user in users:
                cadena += user[1]+"<br>"
        return cadena

    def on_login(self, email):
        """Called on successful login"""
    
    def on_logout(self, email):
        """Called on logout"""
    
    def get_loginform(self, email=None, msg=""):
        html = env.get_template('login.html')
        return html.render(ingresaA="active", msg=msg, email=email)
    
    @cherrypy.expose
    @cherrypy.tools.allow(methods=['GET', 'POST'])
    def login(self, email=None, password=None, tipo=None):
        try:
            u = cherrypy.session.get(SESSION_KEY)
        except Exception, e:
            u = None
        if u:
            send_to(u)
        if cherrypy.request.method == 'GET' :
            if email is None or password is None:
                return self.get_loginform("")
        if cherrypy.request.method == 'POST' :
            error_msg = check_credentials(email, password, tipo)
            if error_msg:
                return self.get_loginform(email, error_msg)
            else:
                cherrypy.session[SESSION_KEY] = cherrypy.request.login = email
                self.on_login(email)
                from_page = cherrypy.session[SESSION_PAGE]
                raise cherrypy.HTTPRedirect(from_page)
    
    @cherrypy.expose
    def logout(self, from_page="/"):
        sess = cherrypy.session
        email = sess.get(SESSION_KEY, None)
        sess[SESSION_KEY] = None
        if email:
            cherrypy.request.login = None
            self.on_logout(email)
        raise cherrypy.HTTPRedirect(from_page or "/")

    @cherrypy.expose
    def dummy(self):
        html = env.get_template("dummy.html")
        return html.render()

cherrypy.config.update({'server.socket_host': '0.0.0.0',})
cherrypy.config.update({'server.socket_port': int(os.environ.get('PORT', '5000')),})
cherrypy.quickstart(RuidoVivo(), "" ,"app.conf")