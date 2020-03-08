import bson
from filters import get_list_of_icons

from flask import Blueprint, request
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
    """adding an event"""
    try:
        list_places = retrieve_places_from_db(True, filter_form=False, place_id=False)
    except Exception as e:
        list_places = []
    load_page("event_add")
    return render_template('event/add_event.html', places=list_places, filter=False, google_key=google_key,
                           page="event_add")


@events_bp.route('/edit_events/', defaults={'filter_string': None, 'update_status': None}, methods=['GET', 'POST'])
@events_bp.route('/edit_events/<string:filter_string>/', defaults={'update_status': None}, methods=['GET', 'POST'])
@events_bp.route('/edit_events/<string:filter_string>/<string:update_status>', methods=['GET', 'POST'])
def edit_events(filter_string, update_status):
    """editing an event"""
    if filter_string is None:
        filter_string = 'None'

    filter_form = FilterEventsFrom()

    the_events = retrieve_events_from_db(True, filter_form)
    # set activities in filter form
    activity_choices = unique_activities(the_events)
    filter_form.activity.choices = activity_choices
    load_page("event_edit_list")
    return render_template('event/edit_events.html', events=the_events, filter=filter_string,
                           google_key=google_key, filter_form=filter_form, update=True, status=update_status,
                           page="event_edit_list")


@events_bp.route('/filter_events', defaults={'update': 'false'}, methods=['POST'])
@events_bp.route('/filter_events/<string:update>/', methods=['POST'])
def filter_events(update):
    """filter events"""
    show_modal = False
    event = False
    form = CountMeInForm()
    filter_form = FilterEventsFrom()
    # check if form was valid (there was a bytes type error when using validate_on_submit when age entered
    if request.method == 'POST' and filter_form.is_submitted() and len(filter_form.errors) == 0:
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

    # is filter for updating or list
    try:
        if update == 'false':
            list_events = list(retrieve_events_from_db(False, filter_form))
        else:
            list_events = list(retrieve_events_from_db(True, filter_form))
        # narrow filtering choices down to current list displayed
        activity_choices = unique_activities(list_events)
        filter_form.activity.choices = activity_choices
    except Exception as e:
        list_events = []
    if update == 'true':
        load_page("event_edit_list_filtered")
        return render_template('event/edit_events.html', events=list_events, filter=filter_string,
                               google_key=google_key, filter_form=filter_form, update=True, status=False,
                               page="event_edit_list_filtered")
    else:
        load_page("event_list_filtered")
        return render_template('event/events.html', form=form, events=list_events, filter=filter_string,
                               show_modal=show_modal,
                               google_key=google_key, layer_event=event, filter_form=filter_form,
                               page="event_list_filtered")


@events_bp.route('/get_events/', defaults={'event_id': None, 'filter_string': None}, methods=['GET', 'POST'])
@events_bp.route('/get_events/<string:event_id>/', defaults={'filter_string': None}, methods=['GET', 'POST'])
@events_bp.route('/get_events/<string:event_id>/<string:filter_string>', methods=['GET', 'POST'])
def get_events(event_id, filter_string):
    """get events"""
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
        # need to show the events list
        try:
            list_events = retrieve_events_from_db(False, False)
        except Exception as e:
            load_page("error", "page", e)
            return render_template('error.html', reason=e, page="error")

        activity_choices = unique_activities(list_events)
        filter_form.activity.choices = activity_choices
        # form is count me in layer
        if form.email.errors:
            show_modal = True
        if event_id is not None and bson.objectid.ObjectId.is_valid(event_id):
            the_event = mongo.db.events.find_one({'_id': ObjectId(event_id)})
            if the_event is not None:
                show_modal = True
                # put event into format the event_layer macro is expecting
                event = mini_event(the_event)
        page = "event_list"
        if show_modal:
            page = "event_join"

        load_page(page)
        return render_template('event/events.html', form=form, events=list_events, filter=filter_string,
                               show_modal=show_modal,
                               google_key=google_key, layer_event=event, filter_form=filter_form, page=page)


@events_bp.route('/new_event/<string:place_id>/', defaults={'status': False}, methods=['GET', 'POST'])
@events_bp.route('/new_event/<string:place_id>/<string:status>/', methods=['GET', 'POST'])
def new_event(place_id, status):
    """add event"""
    form = EventForm()
    # set choices for form select elements
    form.address.country.choices = country_choice_list()
    icons = get_list_of_icons()
    the_place = mongo.db.places.find_one(ObjectId(place_id))

    if form.validate_on_submit():
        # all is good with the post based on PlaceForm wftForm validation
        event = {'place_id': ObjectId(place_id), 'attendees': []}
        return push_event_to_db(form, event)

    # there were errors
    load_page("event_add")
    return render_template('event/new_event.html', form=form, icons=icons, place=the_place, status=status,
                           page="event_add")


@events_bp.route('/update_event/<string:event_id>/', methods=['GET', 'POST'])
def update_event(event_id):
    """update event"""
    form = EventForm()
    # set choices for form select elements
    form.address.country.choices = country_choice_list()
    icons = get_list_of_icons()

    try:
        # get list of ALL events
        list_events = list(retrieve_events_from_db(True, False, event_id))
    except Exception as e:
        load_page("error", "page", e)
        return render_template('error.html', reason=e, page="error")

    if form.validate_on_submit():
        # all is good with the form
        return push_event_to_db(form, list_events[0])

    elif list_events is not None and len(form.errors) == 0:
        # pre populate form
        event = list_events[0]
        form.has_event.data = True
        form.event_name.data = event['event_name'].title()
        form.event_start_datetime.data = event['date_time_range']

        form.activity_name.data = event['activity_name']
        form.activity_icon.data = event['activity_icon']
        form.details.data = event['details']
        form.age_limit.data = event['age_limit']
        form.price_for_non_members.data = event['price_for_non_members']
        form.max_attendees.data = event['max_attendees']
        form.share.data = event['share']

        # pre populate address
        if 'event_address' in event.keys() and event['event_address'] != "" and len(event['event_address']) > 0:
            form.address.address_line_1.data = event['address-address_line_1'].title()
            if 'address-address_line_2'  in  event.keys():
                form.address.address_line_2.data = event['address-address_line_2'].title()
            form.address.city.data = event['address-city'].title()
            form.address.state.data = event['address-state'].title()
            form.address.postal_code.data = event['address-postal_code']
            if 'address-postal_code' in event.keys():
                form.address.country.data = event['country_id']
            form.address.has_address.data = True
        else:
            form.address.has_address.data = False

    load_page("event_update")
    return render_template('event/update_event.html', events=list_events, form=form, update=True, icons=icons,
                           page="event_update")
