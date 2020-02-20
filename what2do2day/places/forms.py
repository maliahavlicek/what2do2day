import re
from flask_wtf import FlaskForm
from wtforms import (StringField,
                     TextAreaField,
                     BooleanField,
                     ValidationError,
                     HiddenField,
                     FormField,)
from wtforms.validators import (DataRequired,
                                Email,
                                Length,
                                URL,
                                Optional)
from what2do2day.reviews.forms import ReviewForm
from what2do2day.addresses.forms import AddressForm
from what2do2day.events.forms import EventForm


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
