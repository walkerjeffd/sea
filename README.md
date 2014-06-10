Stormwater Event Assistant (SEA)
========================================

[Jeff Walker](http://walkerjeff.com)  
Created: 2014-05-20

The Stormwater Event Assistant is a web application for planning stormwater event sampling programs.

The application is built using [flask](http://flask.pocoo.org/).

## Set Up

Create and activate a virtualenv. Install dependencies

```
pip install -r requirements.txt
```

Edit `config.py` with application settings.

## Run Development Server

```
python manage.py runserver -r -d
```

## Setting up Heroku

make sure Procfile contains this line:

    web: gunicorn manage:app

login to heroku, enter username and password

    heroku login

create application where <app_name> is the name of the heroku application (e.g. open-water-demo)

    heroku create <app_name>

add PostgreSQL database addon

    heroku addons:add heroku-postgresql:dev

promote PostgreSQL database (sets the URI to DATABASE_URL), note replace <COLOR>

    heroku pg:promote HEROKU_POSTGRESQL_<COLOR>_URL

set environmental variables on heroku (see above, do all *except* DATABASE_URL)

    heroku config:set NAME=value

make sure requirements.txt exists in top level, which Heroku uses to install dependencies

add [buildpack for GEOS](https://github.com/JasonSanford/heroku-buildpack-python-geos) (used by shapely)

    heroku config:set BUILDPACK_URL=git://github.com/JasonSanford/heroku-buildpack-python-geos.git
    heroku config:set LIBRARY_PATH=/app/.heroku/vendor/lib:vendor/geos/geos/lib:vendor/proj/proj/lib:vendor/gdal/gdal/lib
    heroku config:set LD_LIBRARY_PATH=/app/.heroku/vendor/lib:vendor/geos/geos/lib:vendor/proj/proj/lib:vendor/gdal/gdal/lib

push to Heroku using git

    git push heroku master

run deploy command

    heroku run python manage.py deploy

restart heroku

    heroku restart

review logs

    heroku logs

