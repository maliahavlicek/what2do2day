
import re
from flask_wtf import FlaskForm
from wtforms import (StringField,
                     TextAreaField,
                     SelectField,
                     BooleanField,
                     ValidationError,
                     HiddenField,
                     FormField, IntegerField, SelectMultipleField)
from wtforms.validators import (DataRequired,
                                Email,
                                Length,
                                URL,
                                Optional,
                                NumberRange)

from what2do2day.templates.validators import validate_datetime, validate_daterange
from .reviews.forms import ReviewForm
from .addresses.forms import AddressForm, RequiredIf


class EventForm(FlaskForm):
    has_event = BooleanField('Add Event', default=True)

    event_name = StringField('Name of Event *', [RequiredIf(has_event=True),
                                                 Length(min=1, message='Name of Event is required.')
                                                 ])
    # post from form is 01/29/2020 05:00 - 01/30/2020 23:59
    event_start_datetime = StringField('Date & Time *',
                                       [RequiredIf(has_event=True), Length(min=1, message='Please select a date.'),
                                        validate_datetime])
    address = FormField(AddressForm, 'Address')

    activity_name = StringField('Activity Type', [
        Length(min=1, message="Please enter the activity type.")])
    activity_icon = HiddenField(None, [DataRequired()], default="n")
    details = TextAreaField('Details *', [RequiredIf(has_event=True),
                                          Length(min=1, message="Details are required"),
                                          Length(min=2, message='Your details section is too short'),
                                          Length(max=500, message='Details cannot be longer than 500 characters.')
                                          ])

    age_limit = SelectMultipleField(u'Expected Ages', choices=[('no-limit', 'No Limit'),
                                                               ('0-2', 'Infants'),
                                                               ('3-5', 'Pre-Schoolers'),
                                                               ('6-10', "Elementary Age"),
                                                               ('11-13', 'Middle School'),
                                                               ('14-18', 'High School'),
                                                               ('19-20', 'Young Adult'),
                                                               ('21-plus', '21 and Older')
                                                               ], default='no-limit')

    price_for_non_members = StringField('Price for non-members', [Optional(),
                                                                  Length(min=1, message='Name of Event is required.')])
    max_attendees = IntegerField('Maximum Number of Attendees', [NumberRange(min=1, max=1000,
                                                                             message="You must allow at least 1 to 1,000 people to attend the event.")])
    share = BooleanField('Share with Community', default=True)

    def validate_activity_icon(self, activity_icon):
        """Custom validation to make sure an activity icon was picked"""
        if activity_icon.data == 'n':
            raise ValidationError("Select an icon.")


class FilterEventsFrom(FlaskForm):
    """Filter Events"""

    activity = SelectMultipleField(u'Actvities', default='all')
    age = IntegerField('Age', [Optional(), NumberRange(min=1, max=120, message="A valid age is 0 to 120")])
    filter_date_range = StringField('Date Range',
                                    [Optional(), Length(min=1, message='Please select a date.'),
                                     validate_daterange])

    activity_selection = HiddenField(None, [DataRequired()], default="n")


class CountMeInForm(FlaskForm):
    """Count Me In Form"""

    email = StringField('Email *', [
        Length(min=1, message='Email is required.'),
        Email(message='Not a valid email address.')
    ])


class PlaceForm(FlaskForm):
    """Place Form"""

    email = StringField('Email *', [
        Length(min=1, message='Email is required.'),
        Email(message='Not a valid email address.')
    ])
    name = StringField('Name of Place *', [
        Length(min=1, message='Name of Place is required.')
    ])
    description = TextAreaField('Description *', [
        Length(min=1, message="Description is required"),
        Length(min=2, message='Your description is too short'),
        Length(max=500, message='Descriptions cannot be longer than 500 characters.')
    ])
    activity_name = StringField('Activity Type', [
        Length(min=1, message="Please enter the activity type.")])
    activity_icon = HiddenField(None, [DataRequired()], default="n")
    phone = StringField('Phone', [Optional()])
    website = StringField('Website',
                          [Optional(), URL(message="Please enter a valid website. https://www.example.com.")])
    image_url = StringField('Image Url', [Optional(), URL(message="Please enter a valid url.")])
    address = FormField(AddressForm, 'Address')
    review = FormField(ReviewForm, 'Review')
    event = FormField(EventForm, 'Event')
    share_place = BooleanField('Share with Community', default=True)

    def __init__(self):
        """Initialize the Place Form"""
        super(PlaceForm, self).__init__()

        """Let review form know it should use place email"""
        self.review.use_place_email.value = "y"
        self.review.use_place_email.data = "y"

    def validate_activity_icon(self, activity_icon):
        """Custom validation to make sure an activity icon was picked"""
        if activity_icon.data == 'n':
            raise ValidationError("Select an icon.")

    def validate_name(self, name):
        """Custom validator to make sure name is unique"""
        from what2do2day import mongo
        places = list(mongo.db.places.find({"item.name": name.data}))
        if len(places) > 0:
            raise ValidationError('Place Name already exists.')

    def validate_phone(self, phone):
        if len(phone.data) > 0:
            if not re.match(
                    r'^(?:(?:\+?1\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?$',
                    phone.data):
                raise ValidationError('Please enter a valid phone number, or clear out the entry.')


class ReverseProxied(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        scheme = environ.get('HTTP_X_FORWARDED_PROTO')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        return self.app(environ, start_response)