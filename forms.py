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
    activity_place = SelectField(u'Activity', choices=[('none','Choose Activity')], validators=[])

    def __init__(self):
        """Initialize activity drop down with database entries"""
        super(PlaceForm, self).__init__()

        from app import mongo
        for item in list(mongo.db.activities.find({}, {'name': 1})):
            self.activity_place.choices.append((str(item['_id']), item['name'].capitalize()))

    def validate_activity_place(self, activity_place):
        """Make sure a real selection is made."""
        print("in validate_activity_place")
        print("value is: " + str(activity_place.data))
        if str(activity_place.data) == 'none':
            raise ValidationError('Please select an activity.')

    def validate_name(self, name):
        """Custom validator to make sure name is unique"""
        from app import mongo
        print("in validate_name")
        print("value is: " + str(name.data))
        places = list(mongo.db.places.find({"item.name": name.data}))
        if len(places) > 0:
            raise ValidationError('Place Name already exists.')
