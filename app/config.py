from secrets import token_hex


class Config(object):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SECRET_KEY = token_hex(32)
