
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

class RequiredIf(DataRequired):
    """Validator which makes a field required if another field is set and has a truthy value.
    from thread in https://gist.github.com/devxoul/7638142
    Sources:
        - http://wtforms.simplecodes.com/docs/1.0.1/validators.html
        - http://stackoverflow.com/questions/8463209/how-to-make-a-field-conditionally-optional-in-wtforms
        - https://gist.github.com/devxoul/7638142#file-wtf_required_if-py
    """
    field_flags = ('requiredif',)

    def __init__(self, message=None, *args, **kwargs):
        super(RequiredIf).__init__()
        self.message = message
        self.conditions = kwargs

    # field is requiring that name field in the form is data value in the form
    def __call__(self, form, field):
        for name, data in self.conditions.items():
            other_field = form[name]
            if other_field is None:
                raise Exception('no field named "%s" in form' % name)
            if other_field.data == data and not field.data:
                DataRequired.__call__(self, form, field)
            Optional()(form, field)


class AddressForm(FlaskForm):
    """Address Form"""

    address_line_1 = StringField('Street Address *',
                                 [RequiredIf(has_address=True), Length(min=1, message="Street Address is Required.")])
    address_line_2 = StringField('Address line 2', [Optional()])
    city = StringField('City *', [RequiredIf(has_address=True), Length(min=1)])
    state = StringField('State/Province/Region *', [RequiredIf(has_address=True), Length(min=1)])
    postal_code = StringField('Postal Code', [Optional(), Length(min=1)])
    country = SelectField('Country *', choices=[('none', 'Pick a Country.')])
    has_address = BooleanField('Has Physical Address', default='y')

    def validate_postal_code(self, postal_code):
        """Postal Code Validation"""

        # limited to just alpha,numeric space and dashes for now, would be dependent upon country
        # https://stackoverflow.com/questions/578406/what-is-the-ultimate-postal-code-and-zip-regex
        if len(postal_code.data) > 0:
            """Allow numbers with dashes only """
            if not re.match(r'(?i)^[a-z0-9][a-z0-9\- ]{0,10}[a-z0-9]$', postal_code.data):
                raise ValidationError('Please enter a valid postal code.')

    def validate_country(self, country):
        """Country validation"""
        # RequiredIf doesn't work for SelectField, must use own validation to detect this combination
        if str(country.data) == 'none' and self.has_address.data:
            raise ValidationError('Please select an option.')


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