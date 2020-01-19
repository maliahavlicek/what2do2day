from wtforms import ValidationError


def validate_address(form, field):
    """See if the address is required or not and if it is valid."""
    has_address_value = form.has_address.data
    print("Value of the has_address checkbox: " + str(has_address_value))
    if has_address_value:
        print(form.address)
        raise ValidationError("Address needs attention.")


def validate_activity(form, field):
    """Make sure a real selection is made."""
    if str(form.activity.data) == 'none':
        raise ValidationError('Please select an activity.')