from .controllers import *
from flask import render_template, Blueprint
from bson.objectid import ObjectId

from what2do2day.addresses.views import country_choice_list
from what2do2day import mongo, google_key
from what2do2day.metrics.views import load_page
from what2do2day.places.forms import PlaceForm

################
#### config ####
################
places_bp = Blueprint('places_bp', __name__, template_folder='templates', static_folder='static')


################
#### routes ####
################
@places_bp.route('/add_place', methods=['GET', 'POST'])
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

        icons = filters.get_list_of_icons()
        load_page("place_add")
        return render_template('place/add_place.html', form=form, icons=icons, page="place_add")


@places_bp.route('/edit_place/', defaults={'status': False}, methods=['GET'])
@places_bp.route('/edit_place/<string:status>', methods=['GET'])
def edit_place(status):
    try:
        list_places = retrieve_places_from_db(True, filter_form=False, place_id=False)
    except Exception as e:
        list_places = []
    load_page("place_edit_list")
    if status:
        if status == "OK":
            load_page("place_update_success", "modal")
        else:
            load_page("place_update_fail", "modal")
    else:
        load_page("place_edit_list")
    return render_template('place/place_edit.html', places=list_places, filter=filters, google_key=google_key,
                           page="place_edit_list", status=status)


@places_bp.route('/get_places/', defaults={'status': False})
@places_bp.route('/get_places/<string:status>/')
def get_places(status):
    try:
        list_places = retrieve_places_from_db(False, filter_form=False, place_id=False)
    except Exception as e:
        list_places = []
    if status:
        if status == "OK":
            load_page("place_add_success", "modal")
        else:
            load_page("place_add_fail", "modal")
    else:
        load_page("place_list")
    return render_template('place/places.html', places=list_places, google_key=google_key, page="place_list",
                           status=status)


@places_bp.route('/update_place/<string:place_id>/', methods=['GET', 'POST'])
def update_place(place_id):
    form = PlaceForm()
    form.address.country.choices = country_choice_list()
    icons = filters.get_list_of_icons()
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
        load_page("error", "page", e)
        return render_template('error.html', reason=e, page="error")

    if form.validate_on_submit():
        # all is good with the post based on PlaceForm wftForm validation
        return push_place_to_db(form)
    load_page("place_update")
    return render_template('place/update_place.html', form=form, icons=icons, update=True, places=places,
                           page="place_update")
