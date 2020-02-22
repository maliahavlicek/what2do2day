import bson
from filters import get_list_of_icons

from flask import Blueprint
from what2do2day.addresses.views import country_choice_list
from what2do2day.places.views import retrieve_places_from_db
from what2do2day.events.forms import EventForm, CountMeInForm, FilterEventsFrom

from .controllers import *
################
#### config ####
################

events_bp = Blueprint('events_bp', __name__, template_folder='templates', static_folder='static')


################
#### routes ####
################
@events_bp.route('/add_event', methods=['GET'])
def add_event():
    try:
        list_places = retrieve_places_from_db(True, filter_form=False, place_id=False)
    except Exception as e:
        list_places = []

    return render_template('event/add_event.html', places=list_places, filter=False, google_key=google_key)


@events_bp.route('/edit_events/', defaults={'filter_string': None, 'update_status': None}, methods=['GET', 'POST'])
@events_bp.route('/edit_events/<string:filter_string>/', defaults={'update_status': None}, methods=['GET', 'POST'])
@events_bp.route('/edit_events/<string:filter_string>/<string:update_status>', methods=['GET', 'POST'])
def edit_events(filter_string, update_status):
    if filter_string is None:
        filter_string = 'None'

    filter_form = FilterEventsFrom()

    the_events = retrieve_events_from_db(True, filter_form)
    activity_choices = unique_activities(the_events)
    filter_form.activity.choices = activity_choices
    return render_template('event/edit_events.html', events=the_events, filter=filter_string,
                           google_key=google_key, filter_form=filter_form, update=True, status=update_status)


@events_bp.route('/filter_events', defaults={'update': 'false'}, methods=['POST'])
@events_bp.route('/filter_events/<string:update>/', methods=['POST'])
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
        activity_choices = unique_activities(list_events)
        filter_form.activity.choices = activity_choices
    except Exception as e:
        list_events = []
    if update == 'true':
        return render_template('event/edit_events.html', events=list_events, filter=filter_string,
                               google_key=google_key, filter_form=filter_form, update=True, status=False)
    else:
        return render_template('event/events.html', form=form, events=list_events, filter=filter_string,
                               show_modal=show_modal,
                               google_key=google_key, layer_event=event, filter_form=filter_form)


@events_bp.route('/get_events/', defaults={'event_id': None, 'filter_string': None}, methods=['GET', 'POST'])
@events_bp.route('/get_events/<string:event_id>/', defaults={'filter_string': None}, methods=['GET', 'POST'])
@events_bp.route('/get_events/<string:event_id>/<string:filter_string>', methods=['GET', 'POST'])
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

        activity_choices = unique_activities(list_events)
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


@events_bp.route('/new_event/<string:place_id>/', defaults={'status': False}, methods=['GET', 'POST'])
@events_bp.route('/new_event/<string:place_id>/<string:status>/', methods=['GET', 'POST'])
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


@events_bp.route('/update_event/<string:event_id>/', methods=['GET', 'POST'])
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
