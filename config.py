import os
from secret import URI
class Config(object):
    TESTING = False
    DEBUG = True
    SECRET_KEY = os.urandom(32)
    URI = URI
    