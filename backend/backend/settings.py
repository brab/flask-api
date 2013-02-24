import os

CSRF_SECRET_KEY = ''
SESSION_KEY = ''

class _Config(object):
    DEBUG = True
    TESTING = False
    SECRET_KEY = CSRF_SECRET_KEY
    CSRF_SESSION_LKEY = SESSION_KEY
    CSRF_ENABLED = True
    PROJECT_DIR = os.path.dirname(__file__)

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'username@gmail.com'
    MAIL_PASSWORD = 'password'
    DEFAULT_MAIL_SENDER = 'User Name<username@gmail.com>'

    ADMINS = ['User Name<username@gmail.com>', ]

class Prod(_Config):
    DEBUG = False
    TESTING = False
    MONGODB_SETTINGS = {
            # MongoLab url
            'host': 'mongodb://USERNAME:PASSWORD@MONGO_LAB_URL',
            }

    S3_BUCKET = 'eventsage-prod'

class Dev(_Config):
    NAME = "Dev"
    DEBUG = True
    MONGODB_SETTINGS = {
            # MongoLab url
            'host': 'mongodb://USERNAME:PASSWORD@MONGO_LAB_URL',
            }

class Local(_Config):
    NAME = "Local"
    DEBUG = True

    # setting to True will cause email not to actually send
    TESTING = DEBUG

    MONGODB_DB = 'flask_api_local'

class Testing(_Config):
    NAME = "Test"
    TESTING = True
    MONGODB_SETTINGS = {
        'db': 'flask_api_testing'
    }
