import re
from flask_wtf import FlaskForm
from wtforms import (StringField,
                     SelectField,
                     BooleanField,
                     ValidationError)
from wtforms.validators import (DataRequired,
                                Length,
                                Optional)




class ReverseProxied(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        scheme = environ.get('HTTP_X_FORWARDED_PROTO')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        return self.app(environ, start_response)
