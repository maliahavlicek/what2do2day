import re
from os import listdir
from os.path import splitext, isfile, join

from jinja2 import filters
from datetime import datetime


def date_only(date):
    """Function takes a datetime object and stringifies it down to MM/DD/YYYY format"""
    try:
        start_date = datetime.strftime(date, '%m/%d/%Y')
    except (TypeError, ValueError) as e:
        start_date = date
        pass
    return start_date


def date_range(date_time_range):
    """expecting MM/DD/YYYY HH:MM - MM/DD/YYYY HH:MM
     startDate startTime - endDate endTime
     """
    try:
        if date_time_range and date_time_range != '' and len(date_time_range) == 35:
            start_date = date_time_range[0:10]
            start_time = date_time_range[11:16]
            end_date = date_time_range[19:29]
            end_time = date_time_range[30:35]

            if start_date == end_date:
                time_str = start_date + ": <br>"
                time_str += datetime.strptime(start_time, "%H:%M").strftime("%-I:%M %p") + " to "
                time_str += datetime.strptime(end_time, "%H:%M").strftime("%-I:%M %p")
            else:
                time_str = start_date + " " + datetime.strptime(start_time, "%H:%M").strftime("%-I:%M %p")
                time_str += "<br>&nbsp;&nbsp;&nbsp;to<br>"
                time_str += end_date + " " + datetime.strptime(end_time, "%H:%M").strftime("%-I:%M %p")

        else:
            time_str = date_time_range
        return time_str
    except (TypeError, ValueError) as e:
        pass
        return date_time_range


def icon_alt(icon_file_name):
    """take an image name strip out file extension and numbers"""
    if isinstance(icon_file_name, str):
        try:
            clean_name = splitext(icon_file_name)[0]
            clean_name = re.sub(r'[0-9]', '', clean_name)
            clean_name = clean_name.replace('-', ' ')
            return re.sub(' +', ' ', clean_name).strip()
        except (TypeError, ValueError) as e:
            pass
            return icon_file_name
    return icon_file_name


def get_list_of_icons():
    icon_path = 'what2do2day/static/assets/images/icons'
    icons = [f for f in listdir(icon_path) if isfile(join(icon_path, f))]
    # need to sort by friendly name
    friendlier = []
    for f in icons:
        friendlier.append({'file': f, 'alt': icon_alt(f)})

    friendlier = sorted(friendlier, key=lambda i: i['alt'])

    res = [sub['file'] for sub in friendlier]

    return res


def myround(*args, **kw):
    try:
        """from https://stackoverflow.com/questions/28458524/how-to-round-to-zero-decimals-if-there-is-no-decimal-value-with-jinja2"""
        # Use the original round filter, to deal with the extra arguments
        res = filters.do_round(*args, **kw)
        # Test if the result is equivalent to an integer and
        # return depending on it
        ires = int(res)
        return res if res != ires else ires

    except (TypeError, ValueError) as e:
        pass
        return None


def time_only(date_time_range):
    try:
        if date_time_range and date_time_range != '' and len(date_time_range) == 35:
            start_date = date_time_range[0:10]
            start_time = date_time_range[11:16]
            end_date = date_time_range[19:29]
            end_time = date_time_range[30:35]
            if end_date == start_date:
                time_str = datetime.strptime(start_time, "%H:%M").strftime("%-I:%M %p") + " to "
                time_str += datetime.strptime(end_time, "%H:%M").strftime("%-I:%M %p")
            else:
                time_str = date_time_range
            return time_str
        else:
            return date_time_range

    except (TypeError, ValueError) as e:
        pass
        return date_time_range
