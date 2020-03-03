from os.path import isfile, join
from flask import Flask, render_template
from flask_pymongo import PyMongo
from flask_wtf.csrf import CSRFProtect, CSRFError

import filters
from .forms import ReverseProxied

app = Flask(__name__, instance_relative_config=True)
app.jinja_env.filters['date_only'] = filters.date_only
app.jinja_env.filters['date_range'] = filters.date_range
app.jinja_env.filters['icon_alt'] = filters.icon_alt
app.jinja_env.filters['myround'] = filters.myround
app.jinja_env.filters['time_only'] = filters.time_only
app.jinja_env.filters['pluralize'] = filters.pluralize

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
from what2do2day.metrics.views import metrics_bp, load_page
from what2do2day.places.views import places_bp
from what2do2day.reviews.views import reviews_bp
from what2do2day.users.views import users_bp

# register the blueprints
app.register_blueprint(addresses_bp)
app.register_blueprint(events_bp)
app.register_blueprint(metrics_bp)
app.register_blueprint(places_bp)
app.register_blueprint(reviews_bp)
app.register_blueprint(users_bp)


@app.route('/', methods=['GET', 'POST'])
@app.route('/home')
def home():
    """ initial/default routing for app is the home page """
    load_page("home")
    return render_template('home.html', page="home")


@app.errorhandler(Exception)
def handle_db_error(e):
    load_page("error", "page", 'Exception')
    return render_template('error.html', reason=e, page="error")


@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    load_page("error", "page", 'CSRF')
    reason="Hmm, the CSRF token is missing. Don't worry we've noted the issue and have our best people looking into it."
    return render_template('error.html', reason=reason, page="error")


# app name
@app.errorhandler(404)
# inbuilt function which takes error as parameter
def not_found(e):
    # defining function
    load_page("error", "page", '404')
    reason="We can't seem to find that page right now. Don't worry we've noted the issue and have the best people working on it."
    return render_template('error.html', reason=reason, page="error")


# app name
@app.errorhandler(500)
# inbuilt function which takes error as parameter
def not_found(e):
    # defining function
    load_page("error", "page", '500')
    reason = "The server was unable to complete your request. Don't worry we've noted the issue and hope to fix is as soon as possible."
    return render_template('error.html', reason=reason, page="error"), 500
