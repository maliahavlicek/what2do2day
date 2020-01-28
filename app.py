import os
import re

from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from os import listdir
from os.path import isfile, join, splitext
from pymongo import WriteConcern
from datetime import datetime

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
        # {
        #   from: 'places',
        #   localField: 'place',
        #   foreignField: '_id',
        #   as: 'place_details'
        # }
        pipeline = [

            {
                "$lookup": {
                    'from': 'places',
                    'localField': 'place',
                    'foreignField': '_id',
                    'as': 'place_details'
                }
            },]
        list_events = list(mongo.db.events.aggregate(pipeline))
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
        return the_place['_id']


def db_add_place(place):
    db = mongo.db.places.with_options(
        write_concern=WriteConcern(w=1, j=False, wtimeout=5000)
    )
    the_place = db.insert_one(place)
    return the_place.inserted_id


def db_add_event(event):
    db = mongo.db.events.with_options(
        write_concern=WriteConcern(w=1, j=False, wtimeout=5000)
    )
    the_event = db.insert_one(event)
    return the_event.inserted_id


def db_add_review(review):
    db = mongo.db.reviews.with_options(
        write_concern=WriteConcern(w=1, j=False, wtimeout=5000)
    )
    the_review = db.insert_one(review)
    return the_review.inserted_id


def get_add_address_id(add):
    """retrieve or create an address based on add"""
    the_address = mongo.db.addresses.find_one(add)
    if the_address is None:
        db = mongo.db.addresses.with_options(
            write_concern=WriteConcern(w=1, j=False, wtimeout=5000)
        )
        the_address = db.insert_one(add)
        return the_address.inserted_id
    else:
        return the_address['_id']


def get_add_user_id(email):
    """retrieve or create a user based on email"""
    the_user = mongo.db.users.find_one({'email': email.lower()})
    if the_user is None:
        db = mongo.db.users.with_options(
            # for production application, we'd want a majority(or 2) value and True for confirmation on writing the data
            write_concern=WriteConcern(w=1, j=False, wtimeout=5000)
        )
        the_user = db.insert_one(
            {'email': email.lower()}
        )
        return the_user.inserted_id
    else:
        return the_user['_id']


@app.route('/add_place', methods=['GET', 'POST'])
def add_place():
    form = PlaceForm()

    if form.validate_on_submit():
        # all is good with the post based on PlaceForm wftForm validation
        return push_place_to_db(form)
    elif (not form.event.data['has_event'] and form.event.errors and not form.email.errors and not form.name.errors
          and not form.description.errors and not form.activity_name.errors and not form.activity_icon.errors
          and not form.phone.errors and not form.website.errors and not form.image_url.errors
          and not form.address.errors and not form.review.errors):
        # if all but event are valid, and event is toggled off, suppress errors and push the place to the db
        return push_place_to_db(form)
    else:
        print('form.email: ' + str(form.email.errors))
        print('form.name: ' + str(form.name.errors))
        print('form.description: ' + str(form.description.errors))
        print('form.activity_name: ' + str(form.activity_name.errors))
        print('form.activity_icon: ' + str(form.activity_icon.errors))
        print('form.phone: ' + str(form.phone.errors))
        print('form.website: ' + str(form.website.errors))
        print('form.image_url: ' + str(form.image_url.errors))
        print('form.address: ' + str(form.address.errors))
        print('form.review: ' + str(form.review.errors))
        print('form.event: ' + str(form.event.errors))

        icons = get_list_of_icons()
        return render_template('place/add_place.html', form=form, icons=icons)


@app.errorhandler(Exception)
def handle_db_error(e):
    return render_template('error.html', reason=e)


@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return render_template('error.html', reason=e), 400


@app.template_filter()
def icon_alt(icon_file_name):
    """take an image name strip out file extension and numbers"""
    clean_name = splitext(icon_file_name)[0]
    clean_name = re.sub(r'[0-9]', '', clean_name)
    clean_name = clean_name.replace('-', ' ')
    return re.sub(' +', ' ', clean_name)


def get_list_of_icons():
    icon_path = 'static/assets/images/icons'
    icons = [f for f in listdir(icon_path) if isfile(join(icon_path, f))]
    return icons


def push_place_to_db(form):
    # unique entries for a place are the name and address, so build that first

    place = {'name': form.name.data.strip().lower()}
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

    # add rest of place to the dictionary
    email = form.email.data.strip().lower()
    place['user'] = get_add_user_id(email)

    # place description
    place['description'] = form.description.data.strip()
    place['phone'] = form.phone.data.strip()
    place['website'] = form.website.data.strip()
    place['image_url'] = form.image_url.data.strip()
    place['share_place'] = form.share_place.data
    place['activity_name'] = form.activity_name.data.strip().lower()
    place['activity_icon'] = form.activity_icon.data

    # now we can add the place
    place_id = db_add_place(place)
    if place_id is None:
        return redirect(url_for(handle_db_error('Failed to add place')))

    # next get review
    has_review = form.review.data['has_review']
    if has_review:
        review = {'place': place_id, 'date': datetime.today(), 'user': get_add_user_id(email),
                  'rating': form.review.data['rating'],
                  'comments': form.review.data['comments'].strip()}
        review_id = db_add_review(review)
        if review_id is None:
            return redirect(url_for(handle_db_error('Failed to add review')))

    has_event = form.event.data['has_event']
    if has_event:
        has_address = form.event.address.data['has_address']
        event_address = {}
        if has_address:
            event_address['address_line_1'] = form.event.address.data['address_line_1'].strip().lower()
            if form.event.address.data['address_line_2']:
                event_address['address_line_2'] = form.event.address.data['address_line_2'].strip().lower()
            event_address['city'] = form.event.address.data['city'].strip().lower()
            if form.event.address.data['postal_code']:
                event_address['postal_code'] = form.event.address.data['postal_code'].strip().lower()
            event_address['country'] = form.event.address.data['country']
            address_id = get_add_address_id(event_address)
            event_address_id = address_id
        else:
            event_address_id = ''
        event = {'place': place_id, 'name': form.event.data['event_name'].strip().lower(),
                 'date_time_range': form.event.data['event_start_datetime'],
                 'activity_name': form.event.activity_name.data.strip().lower(),
                 'activity_icon': form.event.activity_icon.data,
                 'details': form.event.data['details'].strip(), 'age_limit': form.event.data['age_limit'],
                 'price_for_non_members': form.event.data['price_for_non_members'].strip(),
                 'address': event_address_id
                 }
        event_id = db_add_event(event)
        if event_id is None:
            return redirect(url_for(handle_db_error('Failed to add event')))

    return redirect(url_for('get_places'))


if __name__ == '__main__':
    app.run(host=os.getenv("IP", "0.0.0.0"),
            port=int(os.getenv("PORT", "5000")),
            debug=True)
