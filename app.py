import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from forms import PlaceForm
from flask_wtf.csrf import CSRFProtect, CSRFError
from config import Config

app = Flask(__name__, instance_relative_config=False)
app.config.from_object('config.Config')

csrf = CSRFProtect(app)
mongo = PyMongo(app)


def db_issue(e):
    print("mongo.db.client.server_info(): " + mongo.db.client_info() + "error" + e)


@app.route('/')
@app.route('/home')
def home():
    """ initial/default routing for app is the home page """
    return render_template('pages/home.html')


@app.route('/get_events')
def get_events():
    try:
        list_events = list(mongo.db.events.find())
    except Exception as e:
        db_issue(e)
        list_events = []

    return render_template('pages/events/events.html', events=list_events, filter='none')


@app.route('/filter_events', methods=['POST'])
def filter_events():
    try:
        list_events = list(mongo.db.events.find())
    except Exception as e:
        db_issue(e)
        list_events = []
    return render_template('pages/events/events.html', events=list_events, filter='none')


@app.route('/add_event', methods=['GET', 'POST'])
def add_event():
    if request.method == 'POST':
        filters = 'yes'
    else:
        filters = 'none'

    try:
        list_places = list(mongo.db.places.find())
    except Exception as e:
        db_issue(e)
        list_places = []

    return render_template('pages/events/add_event.html', places=list_places, filter=filters)


@app.route('/get_places')
def get_places():
    try:
        list_places = list(mongo.db.places.find())
    except Exception as e:
        db_issue(e)
        list_places = []
    return render_template('pages/places/places.html', places=list_places)


@app.route('/add_place', methods=['GET', 'POST'])
def add_place():
    form = PlaceForm()
    if form.validate_on_submit():
        # all is good with the post based on PlaceForm wftForm validation
        return redirect(url_for('get_places'))

    try:
        list_activities = list(mongo.db.activities.find())
    except Exception as e:
        db_issue(e)
        list_activities = []

    return render_template('pages/places/add_place.html', activities=list_activities, form=form)


def place_custom_validation(form):
    # check place activity
    if form.activity_place.value == "none":
        form.activity_place.errors = ['Please make a selection.']
    return form


@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return render_template('csrf_error.html', reason=e.description), 400


if __name__ == '__main__':
    app.run(host=os.getenv("IP", "0.0.0.0"),
            port=int(os.getenv("PORT", "5000")),
            debug=True)
