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
        if "usuario" not in from_page:
            print "no esta la url"
            cherrypy.session[SESSION_PAGE] = "/usuario/"
        if tipo == "facebook":
            return None
        elif u.password != hashlib.sha1(password).hexdigest():
            return u"Correo y/o contraseña invalido(s)"
    return None
    

def check_auth(*args, **kwargs):
    """A tool that looks in config for 'auth.require'. If found and it
    is not None, a login is required and the entry is evaluated as a list of
    conditions that the user must fulfill"""
    conditions = cherrypy.request.config.get('auth.require', None)
    if conditions is not None:
        print "estamos checando"
        print cherrypy.request.path_info
        email = cherrypy.session.get(SESSION_KEY)
        if email:
            print email
            cherrypy.request.login = email
            for condition in conditions:
                # A condition is just a callable that returns true or false
                if not condition():
                    raise cherrypy.HTTPRedirect("/login")
                else:
                    raise cherrypy.HTTPRedirect(cherrypy.request.path_info)
        else:
            cherrypy.session[SESSION_PAGE] = cherrypy.request.path_info
            print "no hay sesion"
            print cherrypy.session.get(SESSION_PAGE)
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
        # replace with actual check if <email> is in <groupname>
        return cherrypy.request.login == 'joe' and groupname == 'admin'
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
        raise cherrypy.HTTPRedirect("/usuario/")
    else:
        raise cherrypy.HTTPRedirect("/administrador/")