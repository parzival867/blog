class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'dev'
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False

    SQLALCHEMY_DATABASE_URI = 'sqlite:///blog.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    pass

class DevConfig(Config):
    DEBUG = True

class TestConfig(Config):
    TESTING = True
