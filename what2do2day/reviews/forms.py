from flask_wtf import FlaskForm
from wtforms import (StringField,
                     TextAreaField,
                     BooleanField,
                     ValidationError,
                     HiddenField,
                     RadioField)
from wtforms.validators import (DataRequired,
                                Email,
                                Length)

from what2do2day.templates.validators import validate_rating, catch_xss
from what2do2day.addresses.forms import RequiredIf


class ReviewForm(FlaskForm):
    """Review Form"""

    has_review = BooleanField('Add Review', default=True)
    author = StringField('Author Email *',
                         [RequiredIf(use_place_email='n'), Length(min=1, message='Email is required.'),
                          Email(message='Not a valid email address.'),
                          catch_xss])
    rating = RadioField('Rating *',
                        choices=[('none', 'none'), ('1', 'Bad: 1-star'), ('2', 'Poor: 2-star'), ('3', 'Fair: 3-star'),
                                 ('4', 'Good: 4-star'),
                                 ('5', 'Excellent: 5-star')], default='none', validators=[validate_rating])
    comments = TextAreaField('Comments *',
                             [RequiredIf(has_review=True), Length(min=1, message='Please enter your review.'),
                              Length(max=500, message='Comments cannot be longer than 500 characters.'),
                              catch_xss])
    use_place_email = HiddenField(None, [DataRequired()], default="n")
    share = BooleanField('Share with Community', default=True)

    def validate_author(self, author):
        if self.has_review.data and str(self.use_place_email.data) == 'n' and len(str(author.data)) < 0:
            raise ValidationError(" you must enter an author")
