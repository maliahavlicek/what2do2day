import re
from flask_wtf import FlaskForm
from wtforms import (StringField,
                     TextAreaField,
                     HiddenField,
                     SubmitField,
                     DateField,
                     SelectField,
                     BooleanField,
                     ValidationError,
                     FormField)
from wtforms.validators import (DataRequired,
                                Email,
                                Length,
                                URL,
                                Optional)

from templates.validators import validate_option_not_none, validate_address


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

    address_line_1 = StringField('Street Address *', [Length(min=1, message="Street Address is Required.")])
    address_line_2 = StringField('Address line 2', [Optional()])
    city = StringField('City *', [Length(min=1)])
    state = StringField('State/Province/Region *', [Length(min=1)])
    postal_code = StringField('Postal Code *', [])
    country = SelectField('Country *', choices=[('none', 'Pick a Country.')], validators=[validate_option_not_none])

    def validate_postal_code(self, postal_code):
        """Postal Code Validation"""

        if len(postal_code.data) > 0:
            """Allow numbers with dashes only """
            if not re.match(r'^(?=.*[09]).*[- 0-9]+$'):
                raise ValidationError('Please enter a valid postal code.')


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
        Length(min=2, message='Your description is too short')
    ])
    activity = SelectField(u'Activity *', choices=[('none', 'Choose Activity')], validators=[validate_option_not_none])
    phone = StringField('Phone', [Optional()])
    website = StringField('Website',
                          [Optional(), URL(message="Please enter a valid website. https://www.example.com.")])
    image_url = StringField('Image Url', [Optional(), URL(message="Please enter a valid url.")])
    has_address = BooleanField('Has Physical Address', default=True, validators=[validate_address])
    address = FormField(AddressForm, 'Address')

    def __init__(self):
        """Initialize activity drop down with database entries"""
        super(PlaceForm, self).__init__()

        from app import mongo
        for item in list(mongo.db.activities.find({}, {'name': 1})):
            self.activity.choices.append((str(item['_id']), item['name'].capitalize()))

        for item in list(mongo.db.countries.find({}, {'country': 1})):
            self.address.country.choices.append((
                str(item['_id']),
                str(item['country']).capitalize()
            ))

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
