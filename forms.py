import re

import pymongo
from flask_wtf import FlaskForm
from wtforms import (StringField,
                     TextAreaField,
                     SelectField,
                     BooleanField,
                     ValidationError,
                     HiddenField,
                     RadioField,
                     FormField, DateTimeField)
from wtforms.validators import (DataRequired,
                                Email,
                                Length,
                                URL,
                                Optional,
                                NumberRange)

from templates.validators import validate_option_not_none
from wtforms.widgets import HiddenInput


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


class ReviewForm(FlaskForm):
    """Review Form"""

    author = StringField('Author Email *',
                         [RequiredIf(use_place_email=False), Length(min=1, message='Email is required.'),
                          Email(message='Not a valid email address.')])
    rating = RadioField('Rating *',
                        choices=[('1', 'Bad: 1-star'), ('2', 'Poor: 2-star'), ('3', 'Fair: 3-star'),
                                 ('4', 'Good: 4-star'),
                                 ('5', 'Excellent: 5-star')])
    comments = TextAreaField('Comments *', [Length(min=1, message='Please enter your review.'),
                                            Length(max=500, message='Comments cannot be longer than 500 characters.')])
    has_review = BooleanField('Add Review', default=True)
    use_place_email = HiddenField(None, [DataRequired()], default="n")


class EventForm(FlaskForm):
    has_event = BooleanField('Add Event', default=True)
    name = StringField('Name of Event *', [
        Length(min=1, message='Name of Event is required.')
    ])
    start_date_time = DateTimeField('Event Start', format='%m/%d/%Y HH:mm')
    end_date_time = DateTimeField('Event End', format='%m/%d/%Y HH:mm')
    activity = SelectField(u'Activity *', choices=[('none', 'Choose Activity')])
    details = TextAreaField('Details *', [
        Length(min=1, message="Details are required"),
        Length(min=2, message='Your details section is too short'),
        Length(max=500, message='Details cannot be longer than 500 characters.')
    ])
    price_for_non_members = StringField('Price for non-members.', [Optional(),
                                                                   Length(min=1, message='Name of Event is required.')])

    def validate_activity(self, activity):
        """activity validation"""
        # RequiredIf doesn't work for SelectField, must use own validation to detect this combination
        if str(activity.data) == 'none' and self.has_event.data:
            raise ValidationError('Please select an option.')


class PlaceForm(FlaskForm):
    """Place Form"""

    email = StringField('Email *', [
        Length(min=1, message='Email is required.'),
        Email(message='Not a valid email address.')
    ])
    name = StringField('Name of Place *', [
        Length(min=1, message='Name of Places is required.')
    ])
    description = TextAreaField('Description *', [
        Length(min=1, message="Description is required"),
        Length(min=2, message='Your description is too short'),
        Length(max=500, message='Descriptions cannot be longer than 500 characters.')
    ])
    activity = SelectField(u'Activity *', choices=[('none', 'Choose Activity')], validators=[validate_option_not_none])
    phone = StringField('Phone', [Optional()])
    website = StringField('Website',
                          [Optional(), URL(message="Please enter a valid website. https://www.example.com.")])
    image_url = StringField('Image Url', [Optional(), URL(message="Please enter a valid url.")])
    address = FormField(AddressForm, 'Address')
    review = FormField(ReviewForm, 'Review')
    event = FormField(EventForm, 'Event')

    def __init__(self):
        """Initialize the Place Form"""
        super(PlaceForm, self).__init__()

        from app import mongo

        """Populate activities list from db"""
        for item in list(mongo.db.activities.find({}, {"name": 1}).sort('name', pymongo.ASCENDING)):
            self.activity.choices.append((str(item['_id']), item['name'].title()))
            self.event.activity.choices.append((str(item['_id']), item['name'].title()))

        """Populate country list from db"""
        for item in list(mongo.db.countries.find({}, {'country': 1}).sort('country', pymongo.ASCENDING)):
            self.address.country.choices.append((
                str(item['_id']),
                item['country'].replace('&amp;', '&').title()
            ))

        """Let review form know it should use place email"""
        self.review.use_place_email.value = "y"

    def validate_name(self, name):
        """Custom validator to make sure name is unique"""
        from app import mongo
        places = list(mongo.db.places.find({"item.name": name.data}))
        if len(places) > 0:
            raise ValidationError('Place Name already exists.')

    def validate_phone(self, phone):
        if len(phone.data) > 0:
            if not re.match(
                    r'^(?:(?:\+?1\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?$',
                    phone.data):
                raise ValidationError('Please enter a valid phone number, or clear out the entry.')
