import re
from flask_wtf import FlaskForm
from wtforms import (StringField,
                     SelectField,
                     BooleanField,
                     ValidationError)
from wtforms.validators import Length, Optional, DataRequired


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
                                 [RequiredIf(has_address=True),
                                  Length(min=1, message="Street Address is Required."),
                                  Length(max=50, message="Street Address must be less than 50 characters.")])
    address_line_2 = StringField('Address line 2', [Optional(), Length(max=50,
                                                                       message="Address Line 2 must be less than 50 characters.")])
    city = StringField('City *', [RequiredIf(has_address=True), Length(min=1),
                                  Length(max=50, message="City must be less than 50 characters.")])
    state = StringField('State/Province/Region *', [RequiredIf(has_address=True), Length(min=1),
                                                    Length(max=50, message="State must be less than 50 characters.")])
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
