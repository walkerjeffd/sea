from flask import render_template, flash, redirect, url_for
from flask.ext.admin.contrib.sqla import ModelView
from . import main
from .. import admin, db
from ..models import Forecast, Location
from datetime import datetime

AMOUNTS = {
    0: '0.0',
    0.01: '0.01-0.10',
    0.1: '0.10-0.25',
    0.25: '0.25-0.50',
    0.5: '0.50-0.75',
    0.75: '0.75-1.00',
    1: '1.00-1.25',
    1.25: '1.25-1.50',
    1.75: '1.75-2.00',
    2: '2.00-2.50',
    2.5: '2.50-3.00',
    3: '3.00-4.00',
    4: '4.00-5.00',
    5: '5.00-7.00',
    7: '7.00-10.00',
    10: '10.00-15.00',
    15: '15.00-20.00'
}

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/locations')
def locations():
    locations = Location.query.all()
    return render_template('location_list.html', locations=locations)

@main.route('/locations/<int:id>')
def location(id):
    location = Location.query.get_or_404(id)
    return render_template('location_detail.html',
        location=location, now=datetime.utcnow(),
        AMOUNTS=AMOUNTS)

@main.route('/locations/<int:id>/update')
def update_location(id):
    location = Location.query.get_or_404(id)
    if not location.is_outdated(hours=6):
        flash('Last update was performed less than 6 hours ago, wait a while')
        return redirect(url_for('main.location', id=id))
    try:
        location.get_all_forecasts()
    except Exception as e:
        flash('Error occured on server: %s' % (str(e)))
        return redirect(url_for('main.location', id=id))
    flash('Forecast successfully updated.')
    return redirect(url_for('main.location', id=id))

admin.add_view(ModelView(Location, db.session))
admin.add_view(ModelView(Forecast, db.session))