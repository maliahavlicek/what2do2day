import re
from datetime import datetime
from os.path import isfile, join, splitext

import bson
import pymongo
import requests
from bson.objectid import ObjectId
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from flask_wtf.csrf import CSRFProtect, CSRFError
from pymongo import WriteConcern

import filters
from .forms import PlaceForm, EventForm, CountMeInForm, FilterEventsFrom, ReverseProxied

app = Flask(__name__, instance_relative_config=True)
app.jinja_env.filters['date_only'] = filters.date_only
app.jinja_env.filters['date_range'] = filters.date_range
app.jinja_env.filters['icon_alt'] = filters.icon_alt
app.jinja_env.filters['myround'] = filters.myround
app.jinja_env.filters['time_only'] = filters.time_only
if isfile(join('instance', 'flask_full.cfg')):
    app.config.from_pyfile('flask_full.cfg')
else:
    app.config.from_pyfile('flask.cfg')

app.wsgi_app = ReverseProxied(app.wsgi_app)

csrf = CSRFProtect(app)
mongo = PyMongo(app)

google_key = app.config['GOOGLE_MAP_KEY']
search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
details_url = "https://maps.googleapis.com/maps/api/place/details/json"

####################
#### blueprints ####
####################
from what2do2day.addresses.views import addresses_bp
from what2do2day.events.views import events_bp
from what2do2day.places.views import places_bp
from what2do2day.reviews.views import reviews_bp
from what2do2day.users.views import users_bp
# register the blueprints
app.register_blueprint(addresses_bp)
app.register_blueprint(events_bp)
app.register_blueprint(places_bp)
app.register_blueprint(reviews_bp)
app.register_blueprint(users_bp)

@app.route('/')
@app.route('/home')
def home():
    """ initial/default routing for app is the home page """
    return render_template('home.html')


@app.errorhandler(Exception)
def handle_db_error(e):
    return render_template('error.html', reason=e)


@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return render_template('error.html', reason=e), 400
