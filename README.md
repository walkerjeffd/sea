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

## Setting up Dreamhost

add subdomain

create virtualenv

create passenger_wsgi.py

upload via ftp

## Setting up Heroku

**NOTE: CANNOT INSTALL FIONA ON HEROKU**

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

generate secret key

    import os
    os.urandom(24)

    'Z\xe7\x83\xfb"J\xcdJ\xf1\xcb\xc8\xf6\xe7\xc7\x9d\xc1k6\xf4\xf1 S\x1fE'

copy result and set SECRET_KEY env var

    heroku config:set SECRET_KEY=...

make sure requirements.txt exists in top level, which Heroku uses to install dependencies
IMPORTANT: remove fiona from requirements/common.txt temporarily (add it in later)

add [buildpack for GEOS](https://github.com/JasonSanford/heroku-buildpack-python-geos) (used by shapely)

    heroku config:set BUILDPACK_URL=git://github.com/JasonSanford/heroku-buildpack-python-geos.git

    heroku config:set BUILDPACK_URL=git://github.com/dulaccc/heroku-buildpack-geodjango.git

push to Heroku using git

    git push heroku master

update PATH

    heroku config:set PATH=/app/.heroku/python/bin:/usr/local/bin:/usr/bin:/bin:/app/.geodjango/gdal/bin

set library paths

    heroku config:set LIBRARY_PATH=/app/.heroku/vendor/lib:vendor/geos/geos/lib:vendor/proj/lib:vendor/gdal/gdal/lib
    heroku config:set LD_LIBRARY_PATH=/app/.heroku/vendor/lib:vendor/geos/geos/lib:vendor/proj/lib:vendor/gdal/gdal/lib
    heroku config:set CPATH=vendor/geos/geos/include:vendor/proj/include:vendor/gdal/gdal/include
    heroku config:set C_INCLUDE_PATH=vendor/geos/geos/include:vendor/proj/include:vendor/gdal/gdal/include
    heroku config:set CPLUS_INCLUDE_PATH=vendor/geos/geos/include:vendor/proj/include:vendor/gdal/gdal/include

add fiona back into requirements/common.txt

    fiona==1.1.5

run deploy command

    heroku run python manage.py deploy

launch a worker

    heroku ps:scale worker=1

restart heroku

    heroku restart

review logs

    heroku logs

