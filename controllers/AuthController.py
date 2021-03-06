# -*- encoding: UTF-8 -*-
#
# Form based authentication for CherryPy. Requires the
# Session tool to be loaded.
#

import cherrypy
import hashlib
from models import User

SESSION_KEY = 'current_user'
SESSION_PAGE = "from_page"

def check_credentials(email, password, tipo):
    """Verifies credentials for email and password.
    Returns None on success or a string describing the error on failure"""
    # An example implementation which uses an ORM could be:
    u = User.find_by_email(email)
    try:
        from_page = cherrypy.session.get(SESSION_PAGE)
    except Exception, e:
        from_page = "/"
    if from_page is None:
        from_page = "/"
    if u:
        if "user" not in from_page:
            cherrypy.session[SESSION_PAGE] = "/user/"
        if tipo == "facebook":
            return None
        elif u.password != hashlib.sha1(password).hexdigest():
            return u"Correo y/o contraseña invalido(s)"
        return None
    return u"Correo y/o contraseña invalido(s)"
    

def check_auth(*args, **kwargs):
    """A tool that looks in config for 'auth.require'. If found and it
    is not None, a login is required and the entry is evaluated as a list of
    conditions that the user must fulfill"""
    conditions = cherrypy.request.config.get('auth.require', None)
    if conditions is not None:
        email = cherrypy.session.get(SESSION_KEY)
        if email:
            cherrypy.request.login = email
            for condition in conditions:
                # A condition is just a callable that returns true or false
                if not condition():
                    raise cherrypy.HTTPRedirect("/login")
        else:
            cherrypy.session[SESSION_PAGE] = cherrypy.request.path_info
            raise cherrypy.HTTPRedirect("/login")
    
cherrypy.tools.auth = cherrypy.Tool('before_handler', check_auth)

def require(*conditions):
    """A decorator that appends conditions to the auth.require config
    variable."""
    def decorate(f):
        if not hasattr(f, '_cp_config'):
            f._cp_config = dict()
        if 'auth.require' not in f._cp_config:
            f._cp_config['auth.require'] = []
        f._cp_config['auth.require'].extend(conditions)
        return f
    return decorate


# Conditions are callables that return True
# if the user fulfills the conditions they define, False otherwise
#
# They can access the current email as cherrypy.request.login
#
# Define those at will however suits the application.

def member_of(groupname):
    def check():
        if groupname == 'admin':
            try:
                email = cherrypy.session.get(SESSION_KEY)
                admin = Admin.find_by_email(email)
            except Exception, e:
                admin = None
            return admin is not None
        if groupname == 'user':
            try:
                email = cherrypy.session.get(SESSION_KEY)
                user = User.find_by_email(email)
            except Exception, e:
                user = None
            return user is not None
    return check

# def name_is(reqd_email):
#     return lambda: reqd_email == cherrypy.request.login

# These might be handy

def any_of(*conditions):
    """Returns True if any of the conditions match"""
    def check():
        for c in conditions:
            if c():
                return True
        return False
    return check

# By default all conditions are required, but this might still be
# needed if you want to use it inside of an any_of(...) condition
def all_of(*conditions):
    """Returns True if all of the conditions match"""
    def check():
        for c in conditions:
            if not c():
                return False
        return True
    return check

def send_to(usuario):
    if User.find_by_email(usuario):
        raise cherrypy.HTTPRedirect("/user/")
    else:
        raise cherrypy.HTTPRedirect("/admin/")