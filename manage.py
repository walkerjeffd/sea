#!/usr/bin/env python

from app import create_app, db
from app.models import Location, Forecast
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

app = create_app('development')
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, Location=Location, Forecast=Forecast)

manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

@manager.command
def bootstrap():
    """Bootstrap database
    >> python manage.py bootstrap
    """
    location = Location(name='Aberjona River', latitude=42.415167, longitude=-71.132575)
    db.session.add(location)
    db.session.commit()

if __name__ == '__main__':
    manager.run()