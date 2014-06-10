from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.admin import Admin
from flask.ext.moment import Moment
from config import config
import os

bootstrap = Bootstrap()
db = SQLAlchemy()
moment = Moment()
admin = Admin(name='QPF Admin')

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    bootstrap.init_app(app)
    db.init_app(app)
    moment.init_app(app)
    admin.init_app(app)

    if not os.path.exists(app.config['QPF_TAR_FOLDER']):
        os.makedirs(app.config['QPF_TAR_FOLDER'])

    if not os.path.exists(app.config['QPF_SHP_FOLDER']):
        os.makedirs(app.config['QPF_SHP_FOLDER'])

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app