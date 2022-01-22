from os import environ


class Config(object):
    '''
    '''
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    ACCESS_TOKEN_PRIVATE_KEY = environ.get("ACCESS_TOKEN_PRIVATE_KEY")

    DATABASE = environ.get("DATABASE")
    DATABASE_PASSWORD = environ.get("DATABASE_PASSWORD")
    DATABASE_USER = environ.get("DATABASE_USER")
    SQL_HOST = environ.get("SQL_HOST")
    SQL_PORT = environ.get("SQL_PORT")
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{SQL_HOST}:{SQL_PORT}/{DATABASE}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    '''
    '''
    DEBUG = False


class DevelopmentConfig(Config):
    '''
    '''
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    '''
    '''
    TESTING = True


config_options = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}
