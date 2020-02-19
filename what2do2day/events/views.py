from os import listdir
from os.path import isfile, join
from filters import icon_alt

from flask import render_template, Blueprint
from flask import current_app as app
from bson.objectid import ObjectId

from pymongo import WriteConcern
from datetime import datetime, timedelta

from what2do2day import mongo
from what2do2day.forms import ReviewForm

################
#### config ####
################

events_bp = Blueprint('events_bp', __name__, template_folder='templates', static_folder='static')

##########################
#### helper functions ####
##########################



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


################
#### routes ####
################
