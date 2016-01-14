# -*- coding: utf-8 -*-
import cherrypy
import hashlib, os, sys
from jinja2 import *
from mako import *
from models import *
from AuthController import require

SESSION_KEY = 'current_user'

env = Environment(loader=FileSystemLoader('views'))

class UserManager(cherrypy.Tool):
    def __init__(self):
        cherrypy.Tool.__init__(self, 'before_handler',
                               self.load, priority=10)

    def load(self):
        print "entra a load"
        req = cherrypy.request
        print req.path_info
        if req.path_info is "":
            print "si es esta"
            url  = "/usuario/"
        elif "usuario" not in req.path_info:
            url  = "/usuario" + req.path_info
        print "la nueva url"
        print url
        req.path_info = url

cherrypy.tools.user = UserManager()

class UsuarioController(object):

    @cherrypy.expose
    @cherrypy.tools.user()
    @require()
    def index(self):
        return "Has ingresado exitosamente "+ User.find_by_email(cherrypy.session[SESSION_KEY]).name +" <a href=\"/logout\">Salir</a>"

    @cherrypy.expose
    @cherrypy.tools.user()
    @require()
    def dummy(self):
        return "para verlo debes iniciar sesion o no?"

cherrypy.tree.mount(UsuarioController(), "/usuario", "app.conf")