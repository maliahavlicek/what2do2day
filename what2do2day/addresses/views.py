import pymongo
from flask import Blueprint
from pymongo import WriteConcern
from what2do2day import mongo
from what2do2day.maps.views import google_get_goecords

################
#### config ####
################
addresses_bp = Blueprint('addresses_bp', __name__, template_folder='templates', static_folder='static')


##########################
#### helper functions ####
##########################
def country_choice_list():
    country_choices = [('none', 'Pick a Country.')]
    for item in list(mongo.db.countries.find({}, {'country': 1}).sort('country', pymongo.ASCENDING)):
        country_choices.append((
            str(item['_id']),
            item['country'].replace('&amp;', '&').title()
        ))
    return country_choices


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


################
#### routes ####
################
