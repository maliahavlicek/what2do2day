
from flask_wtf import FlaskForm
from wtforms import (StringField,
                     TextAreaField,
                     BooleanField,
                     ValidationError,
                     HiddenField,
                     RadioField)
from wtforms.validators import (DataRequired,
                                Email,
                                Length, Optional)


from what2do2day.templates.validators import validate_rating


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


class ReviewForm(FlaskForm):
    """Review Form"""

    has_review = BooleanField('Add Review', default=True)
    author = StringField('Author Email *',
                         [RequiredIf(use_place_email='n'), Length(min=1, message='Email is required.'),
                          Email(message='Not a valid email address.')])
    rating = RadioField('Rating *',
                        choices=[('none', 'none'), ('1', 'Bad: 1-star'), ('2', 'Poor: 2-star'), ('3', 'Fair: 3-star'),
                                 ('4', 'Good: 4-star'),
                                 ('5', 'Excellent: 5-star')], default='none', validators=[validate_rating])
    comments = TextAreaField('Comments *',
                             [RequiredIf(has_review=True), Length(min=1, message='Please enter your review.'),
                              Length(max=500, message='Comments cannot be longer than 500 characters.')])
    use_place_email = HiddenField(None, [DataRequired()], default="n")
    share = BooleanField('Share with Community', default=True)

    def validate_author(self, author):
        if self.has_review.data and str(self.use_place_email.data) == 'n' and len(str(author.data)) < 0:
            raise ValidationError(" you must enter an author")

