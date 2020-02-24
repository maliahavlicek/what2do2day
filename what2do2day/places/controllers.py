import filters
import re
from flask import render_template, redirect, url_for
from bson.objectid import ObjectId

from pymongo import WriteConcern
from datetime import datetime
from what2do2day.activities.views import get_add_activity_id
from what2do2day.addresses.views import get_add_address_id
from what2do2day.events.controllers import event_unique, db_add_event
from what2do2day.metrics.views import load_page
from what2do2day.reviews.views import db_add_review
from what2do2day.users.views import get_add_user_id
from what2do2day import mongo


##########################
#### helper functions ####
##########################
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


def place_unique(place):
    """try to retrieve place from db via name and/or address id"""
    the_place = mongo.db.places.find_one(place)
    if the_place is None:
        return None
    else:
        return the_place['_id']


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
        return redirect(url_for('places_bp.get_places', status="Place already exists."))
    elif is_unique is not None and update and is_unique != ObjectId(place_id):
        return redirect(url_for('places_bp.edit_place', status="Place already exists."))
    elif is_unique is not None and update and is_unique == ObjectId(place_id):
        place['_id'] = ObjectId(place_id)
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
            load_page("error", "page", "failed to add review.")
            return render_template('error.html', reason='When adding the Place, we failed to add the review.')

    has_event = form.event.data['has_event']
    if has_event:

        # create event object to the point of unique data [place_id, name, date_time_range]
        event = {'place': place_id, 'name': form.event.data['event_name'].strip().lower(),
                 'date_time_range': form.event.data['event_start_datetime']
                 }

        # see if event is in database or not
        is_unique = event_unique(event)
        if is_unique is not None:
            load_page("error", "page", "event already exists.")
            return render_template('error.html', reason='Event already exists.')

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
            load_page("error", "page", "Failed to load event.")
            return render_template('error.html', reason='When adding the place, we could not add the event.')
    if update:
        return redirect(url_for('places_bp.edit_place', status="OK"))
    else:
        return redirect(url_for('places_bp.get_places', status="OK"))


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
