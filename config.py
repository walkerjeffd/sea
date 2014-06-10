import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ABCDEFGHIJKLMNOP'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    QPF_TAR_FOLDER = os.path.join(basedir, 'data', 'tar')
    QPF_SHP_FOLDER = os.path.join(basedir, 'data', 'shp')

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
