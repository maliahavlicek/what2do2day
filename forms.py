from flask_wtf import FlaskForm
from wtforms import (StringField,
                     TextAreaField,
                     SubmitField,
                     PasswordField,
                     DateField,
                     SelectField)
from wtforms.validators import (DataRequired,
                                Email,
                                EqualTo,
                                Length,
                                URL)


class PlaceForm(FlaskForm):
    """Place Form"""

    email = StringField('Email', [
        Email(message='Not a valid email address.'),
        DataRequired()
    ])
    name = StringField('Name', [
        DataRequired()
    ])
