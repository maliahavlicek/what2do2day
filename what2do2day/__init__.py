import re
import time
from datetime import datetime
from os import listdir
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

from what2do2day.reviews.views import reviews_blueprint, db_add_review

# register the blueprints
app.register_blueprint(reviews_blueprint)


def db_issue(e):
    print("mongo.db.client.server_info(): " + mongo.db.client_info() + "error" + e)


@app.route('/')
@app.route('/home')
def home():
    """ initial/default routing for app is the home page """
    return render_template('home.html')


def retrieve_events_from_db(update, filter_form=False, event_id=False):
    # join the activities and places to the events database and flatten it down so we don't have to dig for values

    query = []
    activities = []
    age_choices = {
        'no-limit': [0, 120],
        '0-2': [0, 2],
        '3-5': [3, 5],
        '6-10': [6, 10],
        '11-13': [11, 15],
        '14-18': [14, 18],
        '19-20': [19, 20],
        '21-plus': [21, 120]
    }
    ages = []
    filter_start_date = False
    filter_end_date = False

    # check if any filtering is required
    if filter_form:
        # check for activities in the filter_form
        if filter_form.activity_selection.data != "n":
            for item in filter_form.activity_selection.data.split("~"):
                if item != "n":
                    activity = item.split(":")
                    the_activity = mongo.db.activities.find_one({'name': activity[0].lower(), 'icon': activity[1]})
                    if the_activity is not None:
                        activities.append(the_activity['_id'])
                        query.append({"$match": {'activity': {'$in': activities}}})
                    else:
                        pass
        if filter_form.filter_date_range.data is not None and filter_form.filter_date_range.data != "":
            filter_start_date = datetime.strptime(filter_form.filter_date_range.data[0:10], '%m/%d/%Y')
            filter_end_date = datetime.strptime(filter_form.filter_date_range.data[14:24], '%m/%d/%Y')
        if filter_form.age.data:
            for age_limit, age_range in age_choices.items():
                min = age_range[0]
                max = age_range[1]
                if filter_form.age.data >= min and filter_form.age.data <= max:
                    ages.append(age_limit)

    # when updating, we see all events, for normal view, ony show those that are shared
    if not update:
        query.append(
            {"$match": {'share': True}})

    # check if an event id is coming in
    if event_id:
        query.append(
            {"$match": {'_id': ObjectId(event_id)}})

    query.append({
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
            'address_id': '$address',
            'share': '$share'
        }})

    # check for a date range in the filter_form
    if filter_end_date and filter_start_date:
        query.append({
            "$match": {'start_date': {"$gte": filter_start_date, "$lte": filter_end_date}}
        })

    if len(ages) > 0:
        query.append({'$match': {'age_limit': {"$in": ages}}})

    # normal view suppress past events from view
    if not update:
        today = datetime.today()
        query.append(
            {"$match": {'start_date': {"$gte": today}}})
    query.append({"$sort": {'start_date': 1}})
    query.append({
        "$lookup": {
            'from': 'places',
            'localField': 'place_id',
            'foreignField': '_id',
            'as': 'place_details',
        }})
    query.append({
        "$lookup": {
            'from': 'activities',
            'localField': 'activity_id',
            'foreignField': '_id',
            'as': 'event_activity'
        }})
    query.append({
        "$lookup": {
            'from': 'addresses',
            'localField': 'address_id',
            'foreignField': '_id',
            'as': 'event_address'
        }})
    query.append({
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
            }}})
    query.append({
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
            }}})
    query.append({
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
            }}})
    # normal view suppress events with unshared places from view
    if not update:
        query.append({"$match": {'place-share_place': True}})

    list_events = list(mongo.db.events.aggregate(
        query
    ))

    for event in list_events:
        if 'address-country' in event.keys():
            country_id = event['address-country']
            event['country_id'] = country_id
            country = mongo.db.countries.find_one({"_id": ObjectId(country_id)})
            if country is not None:
                event['address-country'] = country['country']
                if 'event_address' in event.keys():
                    event['event_address'][0]['country'] = country['country']

    return list_events


def unique_activities(update="false"):
    activities = []
    ids = {}
    if update == "false":
        events = retrieve_events_from_db(False)
    else:
        events = retrieve_events_from_db(True)
    for event in events:
        new_id = event['activity_id']
        if new_id not in ids.keys():
            ids[new_id] = new_id
            activities.append({'icon': event['activity_icon'], 'name': event['activity_name']})
    return activities


@app.route('/get_events/', defaults={'event_id': None, 'filter_string': None}, methods=['GET', 'POST'])
@app.route('/get_events/<string:event_id>/', defaults={'filter_string': None}, methods=['GET', 'POST'])
@app.route('/get_events/<string:event_id>/<string:filter_string>', methods=['GET', 'POST'])
def get_events(event_id, filter_string):
    show_modal = False
    event = False
    form = CountMeInForm()
    filter_form = FilterEventsFrom()

    if filter_string is None:
        filter_string = 'None'

    if form.validate_on_submit():
        # all is good with the post based on CountMeInForm wftForm validation
        return add_attendee(form, ObjectId(event_id), filter_form, filter_string)

    else:
        try:
            list_events = retrieve_events_from_db(False, False)
        except Exception as e:
            return render_template('error.html', reason=e)

        activity_choices = unique_activities()
        filter_form.activity.choices = activity_choices

        if form.email.errors:
            show_modal = True
        if event_id is not None and bson.objectid.ObjectId.is_valid(event_id):
            the_event = mongo.db.events.find_one({'_id': ObjectId(event_id)})
            if the_event is not None:
                show_modal = True
                event = mini_event(the_event)

        return render_template('event/events.html', form=form, events=list_events, filter=filter_string,
                               show_modal=show_modal,
                               google_key=google_key, layer_event=event, filter_form=filter_form)


@app.route('/edit_place/', methods=['GET'])
def edit_place():
    try:
        list_places = retrieve_places_from_db(True, filter_form=False, place_id=False)
    except Exception as e:
        db_issue(e)
        list_places = []

    return render_template('place/place_edit.html', places=list_places, filter=filters, google_key=google_key)


@app.route('/edit_events/', defaults={'filter_string': None, 'update_status': None}, methods=['GET', 'POST'])
@app.route('/edit_events/<string:filter_string>/', defaults={'update_status': None}, methods=['GET', 'POST'])
@app.route('/edit_events/<string:filter_string>/<string:update_status>', methods=['GET', 'POST'])
def edit_events(filter_string, update_status):
    if filter_string is None:
        filter_string = 'None'

    filter_form = FilterEventsFrom()

    activity_choices = unique_activities("true")
    filter_form.activity.choices = activity_choices

    the_events = retrieve_events_from_db(True, filter_form)
    return render_template('event/edit_events.html', events=the_events, filter=filter_string,
                           google_key=google_key, filter_form=filter_form, update=True, status=update_status)


def push_event_to_db(form, event):
    # create a cleaned up event object to the point of unique data [place_id, name, date_time_range]
    new_event = {'place': event['place_id'], 'name': form.data['event_name'].strip().lower(),
                 'date_time_range': form.data['event_start_datetime']
                 }

    # make sure event is unique if adding (place_id, name, date_time_range combo does not already exist in database)
    if '_id' not in event.keys():
        mongo.db.events.find_one(new_event)
        if mongo.db.events is not None:
            status = "An event with the same name, time and place already exists. Please try again."
            return redirect(url_for('new_event', place_id=event['place_id'], status=status))

    # event is unique so format rest of form entries and load to db
    has_address = form.address.data['has_address']
    event_address = {}
    if has_address:
        event_address['address_line_1'] = form.address.data['address_line_1'].strip().lower()
        if form.address.data['address_line_2']:
            event_address['address_line_2'] = form.address.data['address_line_2'].strip().lower()
        event_address['city'] = form.address.data['city'].strip().lower()
        event_address['state'] = form.address.data['state'].strip().lower()
        if form.address.data['postal_code']:
            event_address['postal_code'] = form.address.data['postal_code'].strip().lower()
        event_address['country'] = form.address.data['country']
        address_id = get_add_address_id(event_address)
        event_address_id = address_id
    else:
        event_address_id = ''

    # see if event's activity is in db or not
    event_activity_id = get_add_activity_id(form.activity_name.data.strip().lower(),
                                            form.activity_icon.data)
    new_event['activity'] = event_activity_id
    new_event['details'] = form.data['details'].strip()
    new_event['age_limit'] = form.data['age_limit']
    new_event['price_for_non_members'] = form.data['price_for_non_members'].strip()
    new_event['address'] = event_address_id
    new_event['max_attendees'] = form.data['max_attendees']
    if 'attendees' in event.keys():
        new_event['attendees'] = event['attendees']
    new_event['share'] = form.share.data

    db = mongo.db.events.with_options(
        write_concern=WriteConcern(w=1, j=False, wtimeout=5000)
    )

    if '_id' in event.keys():
        the_event = db.update_one({"_id": event['_id']}, {"$set": new_event})
    else:
        the_event = db.insert_one(new_event)

    if the_event is None:
        status = "There was a database connectivity issue. Please try again."
    else:
        status = "OK"
    # need to route to edit events maybe show show Success message overlay vs error message overlay
    if '_id' in event.keys():
        return redirect(url_for('edit_events', filter_string='None', update_status=status))
    else:
        return redirect(url_for('new_event', place_id=event['place_id'], status=status))


@app.route('/update_place/<string:place_id>/', methods=['GET', 'POST'])
def update_place(place_id):
    form = PlaceForm()
    form.address.country.choices = country_choice_list()
    icons = get_list_of_icons()
    places = []
    try:
        place = mongo.db.places.find_one({'_id': ObjectId(place_id)})
        if form.validate_on_submit():
            return push_place_to_db(form, True, place_id)
        elif (not form.event.data['has_event'] and form.event.errors and not form.email.errors and not form.name.errors
              and not form.description.errors and not form.activity_name.errors and not form.activity_icon.errors
              and not form.phone.errors and not form.website.errors and not form.image_url.errors
              and not form.address.errors and not form.review.errors):
            # if all but event are valid, and event is toggled off, suppress errors and push the place to the db
            return push_place_to_db(form, True, place_id)

        elif place is not None and len(form.errors) == 0:
            places.append(place)
            """populate event form"""
            form.event.has_event.data = False
            form.review.has_review.data = False
            form.name.data = place['name'].title()
            form.description.data = place['description']
            """get the activity icon & name from the database"""
            activity = mongo.db.activities.find_one({"_id": place['activity']})
            form.activity_name.data = activity['name']
            form.activity_icon.data = activity['icon']
            form.phone.data = place['phone']
            form.website.data = place['website']
            form.image_url.data = place['image_url']
            """get email from the database"""
            email = mongo.db.users.find_one({"_id": place['user']})
            if email is not None:
                form.email.data = email['email']
            """get the address from the database"""
            if place['address'] != "":
                form.address.has_address.data = True
                address = mongo.db.addresses.find_one({'_id': place['address']})
                form.address.address_line_1.data = address['address_line_1']
                if 'address_line_2' in address.keys():
                    form.address.address_line_2.data = address['address_line_2']
                form.address.city.data = address['city']
                form.address.state.data = address['state']
                if 'postal_code' in address.keys():
                    form.address.postal_code.data = address['postal_code']
                form.address.country.data = address['country']

            else:
                form.address.has_address.data = False
            form.share_place.data = place['share_place']


    except Exception as e:
        return render_template('error.html', reason=e)

    if form.validate_on_submit():
        # all is good with the post based on PlaceForm wftForm validation
        return push_place_to_db(form)

    return render_template('place/update_place.html', form=form, icons=icons, update=True, places=places)


@app.route('/update_event/<string:event_id>/', methods=['GET', 'POST'])
def update_event(event_id):
    form = EventForm()
    form.address.country.choices = country_choice_list()
    icons = get_list_of_icons()

    try:
        list_events = list(retrieve_events_from_db(True, False, event_id))
    except Exception as e:
        return render_template('error.html', reason=e)

    if form.validate_on_submit():
        return push_event_to_db(form, list_events[0])

    elif list_events is not None and len(form.errors) == 0:
        event = list_events[0]
        """populate event form"""
        form.has_event.data = True
        form.event_name.data = event['event_name'].title()
        form.event_start_datetime.data = event['date_time_range']

        if form.address.address_line_1.data is not None is not None and form.address.address_line_1.data is not None != "":
            form.address.address_line_1.data = event['address-address_line_1'].title()
            form.address.address_line_2.data = event['address-address_line_2'].title()
            form.address.city.data = event['address-city'].title()
            form.address.state.data = event['address-state'].title()
            form.address.postal_code.data = event['address-postal_code']
            form.address.country.data = event['country_id']
        else:
            form.address.has_address.data = False

        form.activity_name.data = event['activity_name']
        form.activity_icon.data = event['activity_icon']
        form.details.data = event['details']
        form.age_limit.data = event['age_limit']
        form.price_for_non_members.data = event['price_for_non_members']
        form.max_attendees.data = event['max_attendees']
        form.share.data = event['share']

    return render_template('event/update_event.html', events=list_events, form=form, update=True, icons=icons)


def country_choice_list():
    country_choices = [('none', 'Pick a Country.')]
    for item in list(mongo.db.countries.find({}, {'country': 1}).sort('country', pymongo.ASCENDING)):
        country_choices.append((
            str(item['_id']),
            item['country'].replace('&amp;', '&').title()
        ))
    return country_choices


@app.route('/filter_events', defaults={'update': 'false'}, methods=['POST'])
@app.route('/filter_events/<string:update>/', methods=['POST'])
def filter_events(update):
    show_modal = False
    event = False
    form = CountMeInForm()
    filter_form = FilterEventsFrom()

    if filter_form.validate_on_submit():
        # pull out any filtering
        filtering = ""
        if filter_form.activity_selection.data:
            if filter_form.activity_selection.data != "n":
                filtering += "Activities"
        if filter_form.age.data:
            if len(filtering) > 0:
                filtering += ", "
            filtering += "Age"
        if filter_form.filter_date_range.data:
            if len(filtering) > 0:
                filtering += ", "
            filtering += "Date Range: " + str(filter_form.filter_date_range.data)

        filter_string = filtering

    else:
        filter_string = "None"

    try:
        if update == 'false':
            list_events = list(retrieve_events_from_db(False, filter_form))
        else:
            list_events = list(retrieve_events_from_db(True, filter_form))
        activity_choices = unique_activities(update)
        filter_form.activity.choices = activity_choices
    except Exception as e:
        db_issue(e)
        list_events = []
    if update == 'true':
        return render_template('event/edit_events.html', events=list_events, filter=filter_string,
                               google_key=google_key, filter_form=filter_form, update=True, status=False)
    else:
        return render_template('event/events.html', form=form, events=list_events, filter=filter_string,
                               show_modal=show_modal,
                               google_key=google_key, layer_event=event, filter_form=filter_form)


@app.route('/add_event', methods=['GET'])
def add_event():
    try:
        list_places = retrieve_places_from_db(True, filter_form=False, place_id=False)
    except Exception as e:
        db_issue(e)
        list_places = []

    return render_template('event/add_event.html', places=list_places, filter=filters, google_key=google_key)


@app.route('/new_event/<string:place_id>/', defaults={'status': False}, methods=['GET', 'POST'])
@app.route('/new_event/<string:place_id>/<string:status>/', methods=['GET', 'POST'])
def new_event(place_id, status):
    form = EventForm()
    form.address.country.choices = country_choice_list()
    icons = get_list_of_icons()
    the_place = mongo.db.places.find_one(ObjectId(place_id))

    if form.validate_on_submit():
        # all is good with the post based on PlaceForm wftForm validation
        event = {'place_id': ObjectId(place_id), 'attendees': []}
        return push_event_to_db(form, event)

    # there were errors

    return render_template('event/new_event.html', form=form, icons=icons, place=the_place, status=status)


@app.route('/get_places')
def get_places():
    try:
        list_places = retrieve_places_from_db(False, filter_form=False, place_id=False)
    except Exception as e:
        db_issue(e)
        list_places = []
    return render_template('place/places.html', places=list_places, google_key=google_key)


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

    if '_id' in place.keys():
        the_place = db.update_one({"_id": place['_id']}, {"$set": place})
        return place["_id"]
    else:
        the_place = db.insert_one(place)
        return the_place.inserted_id








def db_add_event(event):
    db = mongo.db.events.with_options(
        write_concern=WriteConcern(w=1, j=False, wtimeout=5000)
    )
    the_event = db.insert_one(event)
    return the_event.inserted_id


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
    form.address.country.choices = country_choice_list()
    form.event.address.country.choices = country_choice_list()

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


def icon_alt(icon_file_name):
    """take an image name strip out file extension and numbers"""
    if isinstance(icon_file_name, str):
        try:
            clean_name = splitext(icon_file_name)[0]
            clean_name = re.sub(r'[0-9]', '', clean_name)
            clean_name = clean_name.replace('-', ' ')
            return re.sub(' +', ' ', clean_name).strip()
        except (TypeError, ValueError) as e:
            pass
            return icon_file_name
    return icon_file_name


def get_list_of_icons():
    icon_path = 'what2do2day/static/assets/images/icons'
    icons = [f for f in listdir(icon_path) if isfile(join(icon_path, f))]
    # need to sort by friendly name
    friendlier = []
    for f in icons:
        friendlier.append({'file': f, 'alt': icon_alt(f)})

    friendlier = sorted(friendlier, key=lambda i: i['alt'])

    res = [sub['file'] for sub in friendlier]

    return res


def add_attendee(form, event_id, filter_form, filter_string):
    """Count me in form was posted, process it"""
    attendee = get_add_user_id(form.email.data)
    status = "OK"
    message = "Great!. You should be getting an email shortly with the invite."
    show_modal = True

    # see if id is already in list of attendees for the given event
    the_event = mongo.db.events.find_one({"_id": ObjectId(event_id)})

    if the_event is None:
        status = "ERROR"
        message = "Oops. I'm sorry, but the Event is no longer active and I am unable to add you to it."
    else:
        already_attending = attendee in the_event['attendees']
        max_attend = the_event['max_attendees']

        event = mini_event(the_event)

        if already_attending:
            status = "WARNING"
            message = "Opps. It looks like you are already attending this event."
        elif len(the_event['attendees']) >= max_attend:
            status = "WARNING"
            message = "Oh no, it looks like the event reached max capacity."
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

        event = mini_event(the_event)

        list_events = retrieve_events_from_db(False, False)
        activity_choices = unique_activities("false")
        filter_form.activity.choices = activity_choices
        # somehow filter_from activity choices are crap, when going back
        return render_template('event/events.html', form=form, events=list_events, filter=filter_string,
                               show_modal=modal, google_key=google_key, layer_event=event, filter_form=filter_form)


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


def push_place_to_db(form, update=False, place_id=False):
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
    if is_unique is not None and not update:
        return render_template('error.html', reason="Place already exists.", place_id=is_unique), 1200
    elif is_unique != ObjectId(place_id):
        return render_template('error.html', reason="Place already exists.", place_id=is_unique), 1200
    elif is_unique == ObjectId(place_id):
        place['_id']= ObjectId(place_id)
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

    # now we can add the place or update it
    place_id = db_add_place(place)

    # next get review
    has_review = form.review.data['has_review']
    if has_review:
        review = {'place': place_id, 'date': datetime.today(), 'user': get_add_user_id(email),
                  'rating': int(form.review.data['rating']),
                  'comments': form.review.data['comments'].strip(),
                  'share': form.share_place.data}
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
        event['share'] = form.share_place.data

        event_id = db_add_event(event)
        if event_id is None:
            return redirect(url_for(handle_db_error('Failed to add event')))

    return redirect(url_for('get_places'))


def retrieve_places_from_db(update, filter_form=False, place_id=False):
    # join the activities and address to the places database and flatten it down so we don't have to dig for values

    query = []
    activities = []
    ratings = []

    # check if any filtering is required
    if filter_form:
        # check for activities in the filter_form
        if filter_form.activity_selection.data != "n":
            for item in filter_form.activity_selection.data.split("~"):
                if item != "n":
                    activity = item.split(":")
                    the_activity = mongo.db.activities.find_one({'name': activity[0].lower(), 'icon': activity[1]})
                    if the_activity is not None:
                        activities.append(the_activity['_id'])
                        query.append({"$match": {'activity': {'$in': activities}}})
                    else:
                        pass
        if filter_form.rating.data:
            ratings.append(filter_form.rating.data)

    # when updating, we see all places, for normal view, ony show those that are shared
    if not update:
        query.append(
            {"$match": {'share_place': True}})

    query.append({
        "$project": {
            'place_name': "$name",
            'place_id': "$_id",
            'user_id': "$user",
            'image': '$image_url',
            'activity_id': '$activity',
            'description': '$description',
            'address_id': '$address',
            'phone': '$phone',
            'web': '$website',
            'share': '$share_place'
        }})
    query.append({
        "$lookup": {
            'from': 'activities',
            'localField': 'activity_id',
            'foreignField': '_id',
            'as': 'place_activity'
        }})
    query.append({
        "$lookup": {
            'from': 'addresses',
            'localField': 'address_id',
            'foreignField': '_id',
            'as': 'place_address'
        }})
    query.append({
        "$lookup": {
            'from': 'events',
            'localField': 'place_id',
            'foreignField': 'place',
            'as': 'events'
        }})
    query.append({
        "$lookup": {
            'from': 'reviews',
            'localField': 'place_id',
            'foreignField': 'place',
            'as': 'reviews',
        }
    })

    query.append({
        "$replaceRoot": {
            'newRoot': {
                "$mergeObjects":
                    [{"$let": {
                        "vars": {"v": {"$arrayElemAt": ["$place_activity", 0]}},
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
            }}})
    query.append({
        "$replaceRoot": {
            'newRoot': {
                "$mergeObjects":
                    [{"$let": {
                        "vars": {"v": {"$arrayElemAt": ["$place_address", 0]}},
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
            }}})
    query.append({
        "$addFields": {
            "rating_average": {"$avg": "$reviews.rating"}
        }})

    list_places = list(mongo.db.places.aggregate(query))

    for place in list_places:
        if 'address-country' in place.keys():
            country_id = place['address-country']
            place['country_id'] = country_id
            country = mongo.db.countries.find_one({"_id": ObjectId(country_id)})
            if country is not None:
                place['address-country'] = country['country']
                if 'place_address' in place.keys():
                    place['place_address'][0]['country'] = country['country']
                if 'event_address' in place.keys():
                    place['event_address'][0]['country'] = country['country']
        if 'reviews' in place.keys():
            if len(place['reviews']) > 0:
                for review in place['reviews']:
                    the_user = mongo.db.users.find_one({'_id': review['user']})
                    if the_user is not None:
                        the_user = the_user['email']
                        review['user_name'] = re.sub(r'[@][a-zA-Z]+[.][a-zA-Z]+$', '', the_user)
                place['reviews'] = sorted(place['reviews'], key=lambda x: x['date'], reverse=True)
        if 'events' in place.keys():
            if len(place['events']) > 1:
                place['events'] = sorted(place['events'], key=lambda x: filters.date_only(x['date_time_range'][0:10]))

    return list_places


def mini_event(event):
    min_event = {
        '_id': str(event['_id']),
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
            min_event['place_name'] = the_place['name']
        if 'description' in the_place.keys():
            min_event['place_description'] = the_place['description']

    # dates
    min_event['start_date']: event['date_time_range'][0:10]
    min_event['end_date']: event['date_time_range'][19:29]

    return min_event