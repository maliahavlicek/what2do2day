from flask_wtf import FlaskForm
from wtforms import (StringField,
                     TextAreaField,
                     BooleanField,
                     ValidationError,
                     HiddenField,
                     FormField, IntegerField, SelectMultipleField)
from wtforms.validators import (DataRequired,
                                Email,
                                Length,
                                Optional,
                                NumberRange)

from what2do2day.templates.validators import validate_datetime, validate_daterange, catch_xss
from what2do2day.addresses.forms import AddressForm, RequiredIf


class EventForm(FlaskForm):
    has_event = BooleanField('Add Event', default=True)

    event_name = StringField('Name of Event *', [RequiredIf(has_event=True),
                                                 Length(min=1, message='Name of Event is required.'),
                                                 Length(max=50, message="Name must be less than 50 characters."),
                                                 catch_xss
                                                 ])
    # post from form is 01/29/2020 05:00 - 01/30/2020 23:59
    event_start_datetime = StringField('Date & Time *',
                                       [RequiredIf(has_event=True), Length(min=1, message='Please select a date.'),
                                        validate_datetime])
    address = FormField(AddressForm, 'Address')

    activity_name = StringField('Activity Type', [
        Length(min=1, message="Please enter the activity type."),
        Length(max=50, message="Name must be under 50 characters."),
        catch_xss])
    activity_icon = HiddenField(None, [DataRequired()], default="n")
    details = TextAreaField('Details *', [RequiredIf(has_event=True),
                                          Length(min=1, message="Details are required"),
                                          Length(min=2, message='Your details section is too short'),
                                          Length(max=500, message='Details cannot be longer than 500 characters.'),
                                          catch_xss
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
                                                                  Length(min=1, message='Name of Event is required.'),
                                                                  Length(max=50,
                                                                         message="Price must be less than 50 characters."),
                                                                  catch_xss])
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
    age = IntegerField('Age', [Optional(), NumberRange(min=1, max=120, message="A valid age is 0 to 120"), catch_xss])
    filter_date_range = StringField('Date Range',
                                    [Optional(), Length(min=1, message='Please select a date.'),
                                     validate_daterange])

    activity_selection = HiddenField(None, [DataRequired()], default="n")


class CountMeInForm(FlaskForm):
    """Count Me In Form"""

    email = StringField('Email *', [
        Length(min=1, message='Email is required.'),
        Email(message='Not a valid email address.'),
        catch_xss
    ])
