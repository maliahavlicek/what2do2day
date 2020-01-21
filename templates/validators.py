from datetime import datetime, timedelta, date

from wtforms import ValidationError


def validate_address(form, field):
    """See if the address is required or not and if it is valid."""
    has_address_value = form.has_address.data
    print("Value of the has_address checkbox: " + str(has_address_value))
    if has_address_value:
        print(form.address)
        raise ValidationError("Address needs attention.")


def validate_rating(form, field):
    print('VALIDATING RATING...')
    print('has_review: %s', form.has_review.data)
    print('rating : ' + str(form.rating.data))
    if form.has_review.data:
        print('has review is true...')
        if str(form.rating.data) == 'none':
            print('Raise rating exception')
            raise ValidationError('Select a star rating......')


def validate_option_not_none(form, field):
    """Make sure a real selection is made."""
    if str(field.data) == 'none':
        raise ValidationError('Please select an option.')


def validate_datetime(form, field):
    """event date time validation"""
    if not field.data or len(field.data) < 10:
        raise ValidationError("Please select a date.")
    else:
        value = field.data
        # Expecting: MM/DD/YYYY HH:MM - MM/DD/YYYY HH:MM (startDate startTime - endDate endTime)
        if len(value) == 10:
            # have start date only
            raise ValidationError("Please select a start time.")
        elif len(value) == 16:
            # have start date time but no end datetime
            raise ValidationError("Please select an end date and time.")
        elif len(value) == 35:
            # have the right length now check for validity of parts

            # pull apart incoming value to it's pieces
            startDate = value[0:10]
            startTime = value[11:16]
            endDate = value[19:29]
            endTime = value[30:35]

            # check the format of startDate
            if not check_format(startDate, '%m/%d/%Y'):
                raise ValidationError("Incorrect data format, should be MM/DD/YYYY.")

            # check the format of startTime
            if not check_format(startTime, '%H:%M'):
                raise ValidationError("Incorrect time format, should be HH:MM.")

            # check the format of endDate
            if not check_format(endDate, '%m/%d/%Y'):
                raise ValidationError("Incorrect data format, should be MM/DD/YYYY.")

            # check the format of endTime
            if not check_format(endTime, '%H:%M'):
                raise ValidationError("Incorrect time format, should be HH:MM.")

            # check that startDate is not in past
            datetime_start = datetime.strptime(startDate + ' ' + startTime, '%m/%d/%Y %H:%M')
            today = datetime.today()
            if today > datetime_start:
                raise ValidationError("Start is in past.")

            # check that endDate is after startDate
            datetime_end = datetime.strptime(endDate + ' ' + endTime, '%m/%d/%Y %H:%M')
            if datetime_start > datetime_end:
                raise ValidationError("End Date is before Start Date.")

        else:
            raise ValidationError("Invalid Date Time.")


def check_format(value, format_string):
    """# check the format of startDate"""
    try:
        datetime.strptime(value, format_string)
        return True
    except ValueError:
        return False
