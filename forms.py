from flask_wtf import FlaskForm
from wtforms import (StringField,
                     TextAreaField,
                     SubmitField,
                     PasswordField,
                     DateField,
                     SelectField,
                     ValidationError)
from wtforms.validators import (DataRequired,
                                Email,
                                EqualTo,
                                Length,
                                URL)


class PlaceForm(FlaskForm):
    """Place Form"""

    email = StringField('Email', [
        Length(min=1, message='Email is required.'),
        Email(message='Not a valid email address.')
    ])
    name = StringField('Name of Place', [
        Length(min=1, message='Name of Places is required.')
    ])
    description = TextAreaField('Description', [
        Length(min=1, message="Description is required"),
        Length(min=2, message='Your description is too short')
    ])




    def validate_name(self, name):
        """Custom validator to make sure name is unique"""
        from app import mongo
        places = list(mongo.db.places.find({"item.name": name.data}))
        if len(places) > 0:
            raise ValidationError('Place Name already exists.')
