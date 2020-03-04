from bson.objectid import ObjectId
from flask import Blueprint
import requests
import time
from what2do2day import app, mongo, google_key, search_url

################
#### config ####
################
maps_bp = Blueprint('maps_bp', __name__, template_folder='templates', static_folder='static')


##########################
#### helper functions ####
##########################
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
        if app.config['DEBUG']:
            print("Did not get search results. ", e)

    return address

################
#### routes ####
################
