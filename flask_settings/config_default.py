import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + BASE_DIR + '/bucket_list.db'


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + BASE_DIR + '/bucket_list_test.db'









