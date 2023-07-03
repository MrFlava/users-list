from os import path

basedir = path.abspath(path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = f"sqlite:///{ path.join(basedir, 'database.db')}"
SQLALCHEMY_TRACK_MODIFICATIONS = False

try:
    from local_settings import *

except ImportError:
    pass
