class Config(object):
    '''
    '''
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True


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
