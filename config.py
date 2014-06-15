import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ABCDEFGHIJKLMNOP'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
    QPF_TAR_FOLDER = os.path.join(basedir, 'data', 'tar')
    QPF_SHP_FOLDER = os.path.join(basedir, 'data', 'shp')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('SEA_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    QPF_TAR_FOLDER = os.path.join(basedir, 'data', 'tar')
    QPF_SHP_FOLDER = os.path.join(basedir, 'data', 'shp')

class HerokuConfig(ProductionConfig):
    QPF_TAR_FOLDER = os.path.join(basedir, 'tmp', 'tar')
    QPF_SHP_FOLDER = os.path.join(basedir, 'tmp', 'shp')

    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # log to stderr
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.WARNING)
        app.logger.addHandler(file_handler)

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'heroku': HerokuConfig,

    'default': DevelopmentConfig
}
