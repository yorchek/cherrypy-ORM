# -*- coding: utf-8 -*-
import os
import types

import cherrypy
from jinja2 import *

env = Environment(loader=FileSystemLoader('views'))

class Jinja2Tool(cherrypy.Tool):
  """Clase para hacer como en ruby, cada vista con el nombre del método o función que lo llama"""
  
  def __init__(self):
    cherrypy.Tool.__init__(self, 'before_handler', self.render)
  
  def __call__(self, *args, **kwargs):
    if args and isinstance(args[0], (types.FunctionType, types.MethodType)):
      # @template
      args[0].exposed = True
      return cherrypy.Tool.__call__(self, **kwargs)(args[0])
    else:
      # @template()
      def wrap(f):
        f.exposed = True
        return cherrypy.Tool.__call__(self, *args, **kwargs)(f)
      return wrap
  
  def render(self, name = None):
    cherrypy.request.config['template'] = name
    
    handler = cherrypy.serving.request.handler
    def wrap(*args, **kwargs):
      return self._render(handler, *args, **kwargs)
    cherrypy.serving.request.handler = wrap
  
  def _render(self, handler, *args, **kwargs):
    template = cherrypy.request.config['template']
    if not template:
      parts = []
      if hasattr(handler.callable, '__self__'):
        parts.append(handler.callable.__self__.__class__.__name__.lower())
      if hasattr(handler.callable, '__name__'):
        parts.append(handler.callable.__name__.lower())
      # Aquí van algunos modificadores de acceso a las vistas
      if "controller" in parts[0]:
        parts[0] = parts[0][0:-10]
      template = '/'.join(parts)
    
    data     = handler(*args, **kwargs) or {}
    renderer = env.get_template('{0}.html'.format(template))

    return renderer.render(**data) if template and isinstance(data, dict) else data
    

cherrypy.tools.jinja2 = Jinja2Tool()