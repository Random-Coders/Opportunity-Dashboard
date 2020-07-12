import os

class Config(object):
    TESTING = False
    DEBUG = True
    SECRET_KEY = os.urandom(32)