from . import db
from flask import current_app
from datetime import datetime
from qpf import *
import os

class Forecast(db.Model):
    __tablename__ = 'forecasts'
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(16))
    period = db.Column(db.String(8))
    duration = db.Column(db.Integer)
    start_hour = db.Column(db.Integer)
    valid_start = db.Column(db.DateTime())
    valid_end = db.Column(db.DateTime())
    value = db.Column(db.Float)
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    timestamp = db.Column(db.DateTime(), index=True, default=datetime.utcnow)
    latest = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Forecast %s, %d, %d, %s>' % (self.period, self.duration, self.start_hour, str(self.timestamp))

class Location(db.Model):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    forecasts = db.relationship('Forecast', backref='location', lazy='dynamic')

    @property
    def latest_forecasts(self):
        return self.forecasts.filter_by(latest=True).all()

    def get_all_forecasts(self):
        for period, duration, start in QPF_FILES:
            print 'Fetching QPF: %s, %s, %s' % (period, duration, start)
            self.get_forecast(period, duration, start)

    def get_forecast(self, period, duration, start):
        tar_folder = current_app.config['QPF_TAR_FOLDER']
        shp_folder = current_app.config['QPF_SHP_FOLDER']
        folder, filename = fetch_and_extract(period, duration, start, tar_folder=tar_folder, shp_folder=shp_folder)
        qpf = qpf_from_shapefile(os.path.join(folder, filename), self.latitude, self.longitude)
        if qpf is None:
            return None
        print qpf
        valid_times = parse_valid_time(qpf['VALID_TIME'])
        old_forecasts = self.forecasts.filter_by(period=period, duration=duration, start_hour=start, latest=True).all()
        for old_forecast in old_forecasts:
            old_forecast.latest = False
            db.session.add(old_forecast)
        new_forecast = Forecast(
            product=qpf['PRODUCT'],
            period=period,
            duration=duration,
            start_hour=start,
            valid_start=valid_times[0],
            valid_end=valid_times[1],
            value=qpf['QPF'],
            location_id=self.id,
            latest=True)
        db.session.add(new_forecast)
        db.session.commit()

    def archive_forecasts(self):
        for forecast in self.forecasts.filter_by(period=period, duration=duration, start_hour=start, latest=True).all():
            forecast.latest=False
            db.session.add(forecast)
        db.session.commit()

    def last_update(self):
        forecasts = self.latest_forecasts
        last_update = min([f.timestamp for f in forecasts])
        return last_update

    def is_outdated(self, hours=6):
        dt = datetime.utcnow()-self.last_update()
        hours_since_update = dt.days*24 + dt.seconds/60.
        return hours_since_update > hours

    def __repr__(self):
        return '<Location %s>' % self.name
