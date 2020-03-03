from flask import render_template, redirect, url_for
from bson.objectid import ObjectId

from pymongo import WriteConcern
from datetime import datetime
from what2do2day.addresses.views import get_add_address_id
from what2do2day.users.views import get_add_user_id
from what2do2day import app, mongo, google_key
from what2do2day.email.views import email_event
from what2do2day.metrics.views import load_page


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


def unique_activities(events):
    activities = []
    ids = {}

    for event in events:
        new_id = event['activity_id']
        if new_id not in ids.keys():
            ids[new_id] = new_id
            activities.append({'icon': event['activity_icon'], 'name': event['activity_name']})
    return activities


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
            else:
                # send email to attendee
                email_sent = email_event(event, [form.email.data], False, True)
                if email_sent:
                    status = "OK"
                    message = "Great!. You should be getting an email shortly with the invite."
                else:
                    status = "ERROR"
                    message = "Opps, it looks like we are having issues with our email server, can you try again?"

        modal = {
            'status': status,
            'message': message,
            'show': show_modal
        }

        event = mini_event(the_event)

        list_events = retrieve_events_from_db(False, False)
        activity_choices = unique_activities(list_events)
        filter_form.activity.choices = activity_choices
        # somehow filter_from activity choices are crap, when going back
        page = "event_join"
        if modal['status'] == "OK":
            page += "_success"
        else:
            page += "_fail"
        load_page(page)
        return render_template('event/events.html', form=form, events=list_events, filter=filter_string,
                               show_modal=modal, google_key=google_key, layer_event=event, filter_form=filter_form,
                               page=page)


def db_add_event(event):
    db = mongo.db.events.with_options(
        write_concern=WriteConcern(w=1, j=False, wtimeout=5000)
    )
    the_event = db.insert_one(event)
    return the_event.inserted_id


def events_with_attendee_emails_from_db(event_id=False):
    # join the user, event, activity, address and flatten it down so we don't have to dig for values
    query = []

    # check if an event id is coming in
    query.append(
        {"$match": {'_id': ObjectId(event_id)}})

    query.append({
        "$project": {
            'start_date': {
                "$dateFromString": {
                    'dateString': {
                        "$substr": ["$date_time_range", 0, 16]
                    },
                    'format': "%m/%d/%Y %H:%M"}
            },
            'end_date': {
                "$dateFromString": {
                    'dateString': {
                        "$substr": ["$date_time_range", 19, 35]
                    },
                    'format': "%m/%d/%Y %H:%M"}
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

    list_events = list(mongo.db.events.aggregate(query))

    for event in list_events:
        if 'address-country' in event.keys():
            country_id = event['address-country']
            event['country_id'] = country_id
            country = mongo.db.countries.find_one({"_id": ObjectId(country_id)})
            if country is not None:
                event['address-country'] = country['country']
                if 'event_address' in event.keys():
                    event['event_address'][0]['country'] = country['country']
        if 'attendees' in event.keys() and len(event['attendees']) > 0:
            event['user_list'] = list(mongo.db.users.find({'_id': {"$in": event['attendees']}}))

    return list_events


def event_unique(event):
    """try to retrieve event from db via name, date, and place"""
    the_event = mongo.db.events.find_one(event)
    if the_event is None:
        return None
    else:
        return the_event['_id']


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


def push_event_to_db(form, event):
    # create a cleaned up event object to the point of unique data [place_id, name, date_time_range]
    new_event = {'place': event['place_id'], 'name': form.data['event_name'].strip().lower(),
                 'date_time_range': form.data['event_start_datetime']
                 }

    # make sure event is unique if adding (place_id, name, date_time_range combo does not already exist in database)
    if '_id' not in event.keys():
        event_exists = mongo.db.events.find_one(new_event)
        if event_exists is not None:
            status = "An event with the same name, time and place already exists. Please try again."
            return redirect(url_for('events_bp.new_event', place_id=event['place_id'], status=status))
    else:
        event_exists = list(mongo.db.events.find(new_event))
        if event_exists is not None:
            if len(event_exists) > 1:
                status = "An event with the same name, time and place already exists. Please try again."
                return redirect(url_for('events_bp.new_event', place_id=event['place_id'], status=status))
            if len(event_exists) == 1:
                if event_exists[0]['_id'] != event['_id']:
                    status = "An event with the same name, time and place already exists. Please try again."
                    return redirect(url_for('events_bp.new_event', place_id=event['place_id'], status=status))

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
        event['has_address'] = True
        event['address'] = address_id
    else:
        event_address_id = ''
        event['has_address'] = False
        event['address'] = ''

    # see if event's activity is in db or not
    event_activity_id = get_add_activity_id(form.activity_name.data.strip().lower(),
                                            form.activity_icon.data)
    new_event['activity'] = event_activity_id
    new_event['details'] = form.data['details'].strip()
    new_event['age_limit'] = form.data['age_limit']
    # make sure if no-limit in list of age_limits, only have that entry in the list
    if 'no-limit' in new_event['age_limit']:
        new_event['age_limit'] = ['no-limit']
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
        updated_event = events_with_attendee_emails_from_db(event['_id'])
        # need to send update email to attendees if there are any
        email_sent = email_event(updated_event[0], updated_event[0]['user_list'], True, False)

    else:
        the_event = db.insert_one(new_event)

    if the_event is None:
        status = "There was a database connectivity issue. Please try again."
    else:
        status = "OK"
    # need to route to edit events maybe show show Success message overlay vs error message overlay
    if '_id' in event.keys():
        return redirect(url_for('events_bp.edit_events', filter_string='None', update_status=status))
    else:
        return redirect(url_for('events_bp.new_event', place_id=event['place_id'], status=status))


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
                        "$substr": ["$date_time_range", 0, 16]
                    },
                    'format': "%m/%d/%Y %H:%M"}
            },
            'end_date': {
                "$dateFromString": {
                    'dateString': {
                        "$substr": ["$date_time_range", 19, 35]
                    },
                    'format': "%m/%d/%Y %H:%M"}
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
    # sor the results
    query.append({"$sort": {"share": -1, "start_date": 1, "event_name": 1}})

    list_events = list(mongo.db.events.aggregate(query))

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
