from sqlalchemy import create_engine

class Config(object):
    SECRET_KEY='Clave nueva'
    SESSION_COOKIE_SECURE=False

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'magiccookies805@gmail.com' 
    MAIL_PASSWORD = 'rtkj kijr ylfs soxm' 
    MAIL_DEFAULT_SENDER = 'magiccookies805@gmail.com' 
    
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/magiccookies'
    SQLALCHEMY_TRACK_MODIFICATIONS = False