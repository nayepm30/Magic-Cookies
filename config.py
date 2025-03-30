from sqlalchemy import create_engine

class Config(object):
    SECRET_KEY='Clave nueva'
    SESSION_COOKIE_SECURE=False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/magiccookies'
    SQLALCHEMY_TRACK_MODIFICATIONS = False