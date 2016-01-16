# -*- coding: utf-8 -*-
import cherrypy
import hashlib, os, sys
from mako import *
from models import *
from AuthController import require, member_of
from Jinja2Controller import *

SESSION_KEY = 'current_user'

class UserManager(cherrypy.Tool):
    def __init__(self):
        cherrypy.Tool.__init__(self, 'before_handler',
                               self.load, priority=10)

    def load(self):
        req = cherrypy.request
        if req.path_info is "":
            url  = "/user/"
        elif "user" not in req.path_info:
            url  = "/user" + req.path_info
        req.path_info = url

cherrypy.tools.user = UserManager()

class UserController(object):

    @cherrypy.expose
    @cherrypy.tools.user()
    @require()
    @cherrypy.tools.jinja2
    def index(self):
        return  {'user' : User.find_by_email(cherrypy.session[SESSION_KEY]).name}

    @cherrypy.expose
    @cherrypy.tools.user()
    @require(member_of("user"))
    @cherrypy.tools.jinja2
    def dummy(self):
        return {}

cherrypy.tree.mount(UserController(), "/user", "app.conf")