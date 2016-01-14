#-*- coding: utf-8 -*-
import cherrypy
import hashlib, os
from jinja2 import *
from AuthController import require, member_of

env = Environment(loader=FileSystemLoader('views'))

class AdminManager(cherrypy.Tool):
    def __init__(self):
        cherrypy.Tool.__init__(self, 'before_handler',
                               self.load, priority=10)

    def load(self):
        req = cherrypy.request
        url  = "/administrador" + req.path_info
        print url
        req.path_info = url

cherrypy.tools.admin = AdminManager()

SESSION_KEY = 'useremail'
class Administrador(object):

    @cherrypy.expose
    @cherrypy.tools.admin()
    @require(member_of("admin")) 
    def index(self):
        return "Estas en la seccion administrador"

    @cherrypy.expose
    def login(self):
    	try:
            c = cherrypy.session[SESSION_KEY]
        except:
            cherrypy.session[SESSION_KEY] = None
            c = None
        if c is None:
            cadena =  'Para registrarte da click en el boton<form action="/administrador/dologin" method="post">'
            cadena += '<input type="email" name="correo" value="user@example.com" required><br>'
            cadena += '<input type="password" name="contrasena" value="" required><br>'
            cadena += '<button type="submit">Delete</button></form>'
            return cadena
        else:
            raise cherrypy.HTTPRedirect("inicio")

    @cherrypy.expose
    @cherrypy.tools.allow(methods=['POST'])
    def dologin(self, correo, contrasena):
    	cherrypy.session[SESSION_KEY] = correo
    	raise cherrypy.HTTPRedirect("inicio")

    @cherrypy.expose
    def inicio(self):
    	try:
            c = cherrypy.session[SESSION_KEY]
        except:
            cherrypy.session[SESSION_KEY] = None
            c = None
        if c is None:
            raise cherrypy.HTTPRedirect("login")
    	return 'Bienvenido <a href="salir"> Salir </a>'

    @cherrypy.expose
    def salir(self):
    	cherrypy.session[SESSION_KEY] = None
    	raise cherrypy.HTTPRedirect("login")

cherrypy.tree.mount(Administrador(), "/administrador/", "app.conf")