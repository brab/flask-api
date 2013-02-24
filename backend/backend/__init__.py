import os
from flask import Flask, jsonify, send_from_directory
from flask.ext.login import LoginManager
from flask.ext.pymongo import BSONObjectIdConverter
from flask_mail import Mail
from werkzeug.exceptions import HTTPException, default_exceptions

from backend.backend import settings
from backend.backend.models import db
from backend.backend.models.user import User
from backend.backend.views.admin import admin

login_manager = LoginManager()
mail = Mail()

@login_manager.user_loader
def load_user(userid):
    try:
        return User.objects.get(id=userid)
    except:
        return None

def create_app(environment=None):
    '''
    Create an app instance
    '''
    app = Flask('backend')
    app.url_map.converters['ObjectId'] = BSONObjectIdConverter

    # Config app for environment
    if not environment:
        environment = os.environ.get('BACKEND_ENVIRONMENT', 'Local')

    app.config.from_object('backend.backend.settings.%s' % environment)

    # convert exceptions to JSON
    def make_json_error(ex):
        response = jsonify(message=str(ex))
        response.status_code = (ex.code
                if isinstance(ex, HTTPException)
                else 500)
        return response
    for code in default_exceptions.iterkeys():
        app.error_handler_spec[None][code] = make_json_error


    from backend.backend.views.api import api
    app.register_module(api)

    # initialize modules
    admin.init_app(app)
    db.init_app(app)
    login_manager.setup_app(app)
    mail.init_app(app)

    return app
