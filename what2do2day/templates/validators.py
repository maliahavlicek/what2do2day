from datetime import datetime, date

from wtforms import ValidationError
import re


def catch_xss(form, value):
    """Make sure no script tag"""
    if re.match(r'^(.)*(<\s*)(\/*)script', value.data):
        raise ValidationError('Scripting not allowed.')


def check_format(value, format_string):
    """# check the format of startDate"""
    try:
        datetime.strptime(value, format_string)
        return True
    except ValueError:
        return False


def is_date_valid(f_date):
    # check the format of startDate
    if not check_format(f_date, '%m/%d/%Y'):
        raise ValidationError("Incorrect data format, should be MM/DD/YYYY.")
    else:
        pass


def is_time_valid(f_time):
    # check the format of startTime
    if not check_format(f_time, '%H:%M'):
        raise ValidationError("Incorrect time format, should be HH:MM.")
    else:
        pass


def validate_address(form, field):
    """See if the address is required or not and if it is valid."""
    has_address_value = form.has_address.data
    if has_address_value:
        raise ValidationError("Address needs attention.")

def validate_daterange(form, field):
    """event filtering daterange validation"""
    if not field.data or len(field.data) != 23:
        raise ValidationError("Please select a date range.")
    else:
        value = field.data
        # Expecting: MM/DD/YYYY HH:MM - MM/DD/YYYY (startDate - endDate)
        if len(value) != 23:
            # have start date only
            raise ValidationError("Please select a start and ending date")
        else:
            # have the right length now check for validity of parts

            # pull apart incoming value to it's pieces
            startDate = value[0:10]
            endDate = value[14:24]

            # check the format of startDate
            is_date_valid(startDate)

            # check format of endDate
            is_date_valid(endDate)

            # check that startDate is not in past
            daterange_start = datetime.strptime(startDate, '%m/%d/%Y')
            today = date.today()

            if today > daterange_start.date():
                raise ValidationError("Start is in past.")

            # check that endDate is after startDate
            daterange_end = datetime.strptime(endDate, '%m/%d/%Y')
            if daterange_start > daterange_end:
                raise ValidationError("End Date is before Start Date.")


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
            is_date_valid(startDate)

            # check the format of startTime
            is_time_valid(startTime)

            # check the format of endDate
            is_date_valid(endDate)

            # check the format of endTime
            is_time_valid(endTime)

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


def validate_option_not_none(form, field):
    """Make sure a real selection is made."""
    if str(field.data) == 'none':
        raise ValidationError('Please select an option.')


def validate_rating(form, field):
    if form.has_review.data and str(form.rating.data) == 'none':
        raise ValidationError('Select a star rating.')



