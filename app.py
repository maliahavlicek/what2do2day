import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from pymongo import WriteConcern

from forms import PlaceForm, ReviewForm, AddressForm
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
    return render_template('home.html')


@app.route('/get_events')
def get_events():
    try:
        list_events = list(mongo.db.events.find())
    except Exception as e:
        db_issue(e)
        list_events = []

    return render_template('event/events.html', events=list_events, filter='none')


@app.route('/filter_events', methods=['POST'])
def filter_events():
    try:
        list_events = list(mongo.db.events.find())
    except Exception as e:
        db_issue(e)
        list_events = []
    return render_template('event/events.html', events=list_events, filter='none')


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

    return render_template('event/add_event.html', places=list_places, filter=filters)


@app.route('/get_places')
def get_places():
    try:
        list_places = list(mongo.db.places.find())
    except Exception as e:
        db_issue(e)
        list_places = []
    return render_template('place/places.html', places=list_places)


def place_unique(place):
    """try to retrieve place from db via name and/or address id"""
    the_place = mongo.db.places.find_one(place)
    if the_place is None:
        return None
    else:
        return the_place("_id")


def add_place(place):
    db = mongo.db.places.with_options(
        write_concern=WriteConcern(w=1, j=False, wtimeout=5000)
    )
    the_place_id = db.insert_one(place)
    return the_place_id


def get_add_address_id(add):
    """retrieve or create an address based on add"""
    the_address = mongo.db.addresses.find_one(add)
    if the_address is None:
        db = mongo.db.addresses.with_options(
            write_concern=WriteConcern(w=1, j=False, wtimeout=5000)
        )
        the_address_id = db.insert_one(add)
    else:
        the_address_id = the_address['_id']
    return the_address_id


def get_add_user_id(email):
    """retrieve or create a user based on email"""
    the_user = mongo.db.users.find_one({'email': email.lower()})
    if the_user is None:
        db = mongo.db.users.with_options(
            # for production application, we'd want a majority(or 2) value and True for confirmation on writing the data
            write_concern=WriteConcern(w=1, j=False, wtimeout=5000)
        )
        the_user_id = db.insert_one(
            {'email': email.lower()}
        )

    else:
        the_user_id = the_user['_id']
    return the_user_id


@app.route('/add_place', methods=['GET', 'POST'])
def add_place():
    form = PlaceForm()

    if form.validate_on_submit():
        # all is good with the post based on PlaceForm wftForm validation
        place = {}
        # unique entries for a place are the name and address
        # place name

        place['name'] = form.name.data.strip().lower()

        has_address = form.address.data['has_address']
        address = {}
        if has_address:
            address['address_line_1'] = form.address.data['address_line_1'].strip().lower()
            if form.address.data['address_line_2']:
                address['address_line_2'] = form.address.data['address_line_2'].strip().lower()
            address['city'] = form.address.data['city'].strip().lower()
            if form.address.data['postal_code']:
                address['postal_code'] = form.address.data['postal_code'].strip().lower()
            address['country'] = form.address.data['country']
            address_id = get_add_address_id(address)
            place['address'] = address_id
        else:
            place['address'] = ''
        # see if address and name is in db or not
        is_unique = place_unique(place)
        if is_unique is not None:
            return render_template('error.html', reason="Place already exists.", place_id=is_unique), 1200

        # first get user id
        email = form.email.data.strip().lower()
        place['user'] = get_add_user_id(email)

        # place description
        place['description'] = form.description.data.strip()

        place['phone'] = form.phone.data.strip()
        place['website'] = form.website.data.strip()
        place['image_url'] = form.image_url.data.strip()
        place['share_place'] = form.share_place.data



        # now we can add the place
        place_id = add_place(place)

        # next get activity_id
        place['activity'] = form.activity.data

        # next get review

        has_review = form.review.data['has_review']

        has_event = form.event.data['has_event']

        return redirect(url_for('get_places'))
    else:
        print('form.email: ' + str(form.email.errors))
        print('form.name: ' + str(form.name.errors))
        print('form.description: ' + str(form.description.errors))
        print('form.activity: ' + str(form.activity.errors))
        print('form.phone: ' + str(form.phone.errors))
        print('form.website: ' + str(form.website.errors))
        print('form.image_url: ' + str(form.image_url.errors))
        print('form.address: ' + str(form.address.errors))
        print('form.review: ' + str(form.review.errors))
        print('form.event: ' + str(form.event.errors))

        return render_template('place/add_place.html', form=form)


@app.errorhandler(Exception)
def handle_db_error(e):
    return render_template('error.html', reason=e)


@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return render_template('error.html', reason=e), 400


if __name__ == '__main__':
    app.run(host=os.getenv("IP", "0.0.0.0"),
            port=int(os.getenv("PORT", "5000")),
            debug=True)
