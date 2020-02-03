import os
import re
import ast

from flask import Flask, render_template, redirect, request, url_for, json, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from os import listdir
from os.path import isfile, join, splitext
from pymongo import WriteConcern
from datetime import datetime
import requests
import time

from forms import PlaceForm, ReviewForm, AddressForm, CountMeInForm
from flask_wtf.csrf import CSRFProtect, CSRFError
from config import Config

app = Flask(__name__, instance_relative_config=False)
app.config.from_object('config.Config')

csrf = CSRFProtect(app)
mongo = PyMongo(app)

google_key = app.config['GOOGLE_MAP_KEY']
search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
details_url = "https://maps.googleapis.com/maps/api/place/details/json"


def db_issue(e):
    print("mongo.db.client.server_info(): " + mongo.db.client_info() + "error" + e)


@app.route('/')
@app.route('/home')
def home():
    """ initial/default routing for app is the home page """
    return render_template('home.html')


def retrieve_events_from_db():
    # join the activities and places to the events database and flatten it down so we don't have to dig for values
    list_events = list(mongo.db.events.aggregate([
        {
            "$project": {
                'start_date': {
                    "$dateFromString": {
                        'dateString': {
                            "$substr": ["$date_time_range", 0, 10]
                        },
                        'format': "%m/%d/%Y"}
                },
                'end_date': {
                    "$dateFromString": {
                        'dateString': {
                            "$substr": ["$date_time_range", 19, 10]
                        },
                        'format': "%m/%d/%Y"}
                },
                'place_id': "$place",
                'event_name': "$name",
                'event_id': "$_id",
                'activity_id': '$activity',
                'date_time_range': '$date_time_range',
                'details': '$details',
                'age_limit': '$age_limit',
                'price_for_non_members': '$price_for_non_members',
                'attendees': '$attendees',
                'max_attendees': '$max_attendees',
                'address_id': '$address'
            }
        },
        {
            "$sort": {'start_date': 1}
        },
        {
            "$lookup": {
                'from': 'places',
                'localField': 'place_id',
                'foreignField': '_id',
                'as': 'place_details',

            }
        },
        {
            "$lookup": {
                'from': 'activities',
                'localField': 'activity_id',
                'foreignField': '_id',
                'as': 'event_activity'
            }
        },
        {
            "$lookup": {
                'from': 'addresses',
                'localField': 'address_id',
                'foreignField': '_id',
                'as': 'event_address'
            }
        },
        {
            "$replaceRoot": {
                'newRoot': {
                    "$mergeObjects":
                        [{"$let": {
                            "vars": {"v": {"$arrayElemAt": ["$place_details", 0]}},
                            "in": {"$arrayToObject": {
                                "$map": {
                                    "input": {"$objectToArray": "$$v"},
                                    "as": "val",
                                    "in": {
                                        "k": {"$concat": ["place", "-", "$$val.k"]},
                                        "v": "$$val.v"
                                    }}
                            }}
                        }}, "$$ROOT"]
                }
            }
        },
        {
            "$replaceRoot": {
                'newRoot': {
                    "$mergeObjects":
                        [{"$let": {
                            "vars": {"v": {"$arrayElemAt": ["$event_activity", 0]}},
                            "in": {"$arrayToObject": {
                                "$map": {
                                    "input": {"$objectToArray": "$$v"},
                                    "as": "val",
                                    "in": {
                                        "k": {"$concat": ["activity", "_", "$$val.k"]},
                                        "v": "$$val.v"
                                    }}
                            }}
                        }}, "$$ROOT"]
                }
            }
        },
        {
            "$replaceRoot": {
                'newRoot': {
                    "$mergeObjects":
                        [{"$let": {
                            "vars": {"v": {"$arrayElemAt": ["$event_address", 0]}},
                            "in": {"$arrayToObject": {
                                "$map": {
                                    "input": {"$objectToArray": "$$v"},
                                    "as": "val",
                                    "in": {
                                        "k": {"$concat": ["address", "-", "$$val.k"]},
                                        "v": "$$val.v"
                                    }}
                            }}
                        }}, "$$ROOT"]
                }
            }
        },
    ]))

    for event in list_events:
        if 'address-country' in event.keys():
            country_id = event['address-country']
            country = mongo.db.countries.find_one({"_id": ObjectId(country_id)})
            if country is not None:
                event['address-country'] = country['country']
                if 'event_address' in event.keys():
                    event['event_address'][0]['country'] = country['country']

    return list_events


@app.route('/get_events/', defaults={'event_id': None}, methods=['GET', 'POST'])
@app.route('/get_events/<event_id>', methods=['GET', 'POST'])
def get_events(event_id):
    show_modal = False
    event = False
    form = CountMeInForm()
    # TODO look at event_id, retrieve it from DB and add it

    if form.validate_on_submit():
        # all is good with the post based on CountMeInForm wftForm validation
        return add_attendee(form)

    else:
        try:
            list_events = retrieve_events_from_db()
        except Exception as e:
            return render_template('error.html', reason=e)
        if form.email.errors:
            show_modal = True
        if event_id is not None:
            the_event = mongo.db.events.find_one({'_id': ObjectId(event_id)})
            if the_event is not None:
                show_modal = True
                event = mini_event(the_event)

        return render_template('event/events.html', form=form, events=list_events, filter='none', show_modal=show_modal,
                               google_key=google_key, layer_event=event)


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


def event_unique(event):
    """try to retrieve event from db via name, date, and place"""
    the_event = mongo.db.events.find_one(event)
    if the_event is None:
        return None
    else:
        return the_event['_id']


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
        # get google lat and long
        add = google_get_goecords(add)
        db = mongo.db.addresses.with_options(
            write_concern=WriteConcern(w=1, j=False, wtimeout=5000)
        )
        the_address = db.insert_one(add)
        return the_address.inserted_id
    else:
        return the_address['_id']


def get_add_user_id(email):
    """retrieve or create a user based on email"""

    print("IN get_add_user_id. email: ", email)
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


def get_add_activity_id(name, icon):
    """retrieve or create an activity based on name and icon"""
    the_activity = mongo.db.activities.find_one({'name': name.lower(), 'icon': icon})
    if the_activity is None:
        db = mongo.db.activities.with_options(
            # for production application, we'd want a majority(or 2) value and True for confirmation on writing the data
            write_concern=WriteConcern(w=1, j=False, wtimeout=5000)
        )
        the_activity = db.insert_one(
            {'name': name.lower(),
             'icon': icon}
        )
        return the_activity.inserted_id
    else:
        return the_activity['_id']


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


@app.template_filter()
def time_only(date_time_range):
    start_date = date_time_range[0:10]
    start_time = date_time_range[11:16]
    end_date = date_time_range[19:29]
    end_time = date_time_range[30:35]
    if end_date == start_date:
        time_str = datetime.strptime(start_time, "%H:%M").strftime("%-I:%M %p") + " to "
        time_str += datetime.strptime(end_time, "%H:%M").strftime("%-I:%M %p")
    else:
        time_str = date_time_range
    return time_str


@app.template_filter()
def date_range(date_time_range):
    if date_time_range != '':
        start_date = date_time_range[0:10]
        start_time = date_time_range[11:16]
        end_date = date_time_range[19:29]
        end_time = date_time_range[30:35]

        if start_date == end_date:
            time_str = start_date + ": <br>"
            time_str += datetime.strptime(start_time, "%H:%M").strftime("%-I:%M %p") + " to "
            time_str += datetime.strptime(end_time, "%H:%M").strftime("%-I:%M %p")
        else:
            time_str = start_date + " " + datetime.strptime(start_time, "%H:%M").strftime("%-I:%M %p")
            time_str += "<br>&nbsp;&nbsp;&nbsp;to<br>"
            time_str += end_date + " " + datetime.strptime(end_time, "%H:%M").strftime("%-I:%M %p")
    else:
        time_str = date_time_range
    return time_str


@app.template_filter()
def upwrap_json(item):
    unwrapped = ast.literal_eval(item)
    return unwrapped


@app.template_filter()
def mini_event(event):
    min_event = {
        'activity_name': '',
        'activity_icon': '',
        'place_name': '',
        'place_description': '',
        'start_date': '',
        'end_date': '',
        'event_name': event['name'],
        'date_time_range': event['date_time_range'],
        'details': event['details'],
        'age_limit': event['age_limit'],
        'price_for_non_members': event['price_for_non_members'],
        'max_attendees': event['max_attendees'],
        'attendees': len(event['attendees']),
        'event_address': {
            'address_line_1': '',
            'address_line_2': '',
            'city': '',
            'state': '',
            'postal_code': '',
            'country': '',
            'lat': 0,
            'lng': 0,

        }
    }

    # address
    the_address = mongo.db.addresses.find_one(event['address'])
    if the_address is not None:
        if 'address_line_1' in the_address.keys():
            min_event['event_address']['address_line_1'] = the_address['address_line_1']
        if 'address_line_2' in the_address.keys():
            min_event['event_address']['address_line_2'] = the_address['address_line_2']
        if 'city' in the_address.keys():
            min_event['event_address']['city'] = the_address['city']
        if 'state' in the_address.keys():
            min_event['event_address']['state'] = the_address['state']
        if 'postal_code' in the_address.keys():
            min_event['event_address']['postal_code'] = the_address['postal_code']
        if 'country' in the_address.keys():
            min_event['event_address']['country'] = the_address['country']
        if 'lat' in the_address.keys():
            min_event['event_address']['lat'] = the_address['lat']
        if 'lng' in the_address.keys():
            min_event['event_address']['lng'] = the_address['lng']

    # activity
    the_activity = mongo.db.activities.find_one(event['activity'])
    if the_activity is not None:
        if 'icon' in the_activity.keys():
            min_event['activity_icon'] = the_activity['icon']
        if 'name' in the_activity.keys():
            min_event['activity_name'] = the_activity['name']

    # place
    the_place = mongo.db.places.find_one(event['place'])
    if the_place is not None:
        if 'name' in the_place.keys():
            min_event['place_name'] =  the_place['name']
        if 'description' in the_place.keys():
            min_event['place_description'] = the_place['description']

    # dates
    min_event['start_date']: event['date_time_range'][0:10]
    min_event['end_date']: event['date_time_range'][19:29]

    return min_event


def get_list_of_icons():
    icon_path = 'static/assets/images/icons'
    icons = [f for f in listdir(icon_path) if isfile(join(icon_path, f))]
    return icons


def add_attendee(form):
    """Count me in form was posted, process it"""
    attendee = get_add_user_id(form.email.data)
    status = "OK"
    message = "Great!. You should be getting an email shortly with the invite."
    show_modal = True

    # see if id is already in list of attendees for the given event
    event_id = ObjectId(form.attend_event_id.data)
    the_event = mongo.db.events.find_one({"_id": event_id})

    if the_event is None:
        status = "ERROR"
        message = "Oops. I'm sorry, but the Event is no longer active and I am unable to add you to it."
    else:
        already_attending = attendee in the_event['attendees']

        if already_attending:
            status = "WARNING"
            message = "Opps. It looks like you are already attending this event."
        else:
            # add attendee to the list
            db = mongo.db.events.with_options(
                write_concern=WriteConcern(w=1, j=False, wtimeout=5000)
            )
            added_attendee = db.update_one(
                {"_id": ObjectId(event_id)},
                {"$push": {"attendees": attendee}}
            )
            if added_attendee is None:
                status = "ERROR"
                message = "Opps, it looks like we may have lost a bit of data due to network lag time, can you try again?"
    modal = {
        'status': status,
        'message': message,
        'show': show_modal
    }

    list_events = retrieve_events_from_db()
    return render_template('event/events.html', form=form, events=list_events, filter='none', show_modal=modal)


def google_get_goecords(address):
    # get coords for mapping
    add = address['address_line_1']
    if 'address_line_2' in address.keys():
        add += ", " + address['address_line_1']
    add += ", " + address['city']
    add += ", " + address['state']
    if 'postal_code' in address.keys():
        add += " " + address['postal_code']
    country_id = address['country']
    country = mongo.db.countries.find_one({"_id": ObjectId(country_id)})
    if country is not None:
        add += " " + country['country']
    try:

        search_payload = {"key": google_key, "query": add}
        search_req = requests.get(search_url, params=search_payload)

        search_json = search_req.json()
        time.sleep(.3)
        address['lat'] = search_json["results"][0]["geometry"]["location"]["lat"]
        address['lng'] = search_json["results"][0]["geometry"]["location"]["lng"]
        address['one_line'] = add
        address['google_place_id'] = search_json["results"][0]["place_id"]

    except Exception as e:
        print("Did not get search results. ", e)

    return address


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
        address['state'] = form.address.data['state'].strip().lower()
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

    # see if activity is in db or not
    activity_id = get_add_activity_id(form.activity_name.data.strip().lower(), form.activity_icon.data)
    place['activity'] = activity_id

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

        # create event object to the point of unique data [place_id, name, date_time_range]
        event = {'place': place_id, 'name': form.event.data['event_name'].strip().lower(),
                 'date_time_range': form.event.data['event_start_datetime']
                 }

        # see if event is in database or not
        is_unique = event_unique(event)
        if is_unique is not None:
            return render_template('error.html', reason="Event already exists.", event_id=is_unique), 1300

        # event is unique so format rest of form entries and load to db
        has_address = form.event.address.data['has_address']
        event_address = {}
        if has_address:
            event_address['address_line_1'] = form.event.address.data['address_line_1'].strip().lower()
            if form.event.address.data['address_line_2']:
                event_address['address_line_2'] = form.event.address.data['address_line_2'].strip().lower()
            event_address['city'] = form.event.address.data['city'].strip().lower()
            event_address['state'] = form.event.address.data['state'].strip().lower()
            if form.event.address.data['postal_code']:
                event_address['postal_code'] = form.event.address.data['postal_code'].strip().lower()
            event_address['country'] = form.event.address.data['country']
            address_id = get_add_address_id(event_address)
            event_address_id = address_id
        else:
            event_address_id = ''

        # see if event's activity is in db or not
        event_activity_id = get_add_activity_id(form.event.activity_name.data.strip().lower(),
                                                form.event.activity_icon.data)
        event['activity'] = event_activity_id
        event['details'] = form.event.data['details'].strip()
        event['age_limit'] = form.event.data['age_limit']
        event['price_for_non_members'] = form.event.data['price_for_non_members'].strip()
        event['address'] = event_address_id
        event['max_attendees'] = form.event.data['max_attendees']
        event['attendees'] = [get_add_user_id(email)]

        event_id = db_add_event(event)
        if event_id is None:
            return redirect(url_for(handle_db_error('Failed to add event')))

    return redirect(url_for('get_places'))


if __name__ == '__main__':
    app.run(host=os.getenv("IP", "0.0.0.0"),
            port=int(os.getenv("PORT", "5000")),
            debug=True)
