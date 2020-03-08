from pymongo import WriteConcern
from what2do2day import mongo
from what2do2day.events.controllers import retrieve_events_from_db


##########################
#### helper functions ####
##########################
def get_add_activity_id(name, icon):
    """retrieve or create an activity based on name and icon"""
    the_activity = mongo.db.activities.find_one({'name': name.lower(), 'icon': icon})
    if the_activity is None:
        db = mongo.db.activities.with_options(
            # for production application, we'd want a majority(or 2) value and True for confirmation on writing the data
            write_concern=WriteConcern(w=1, j=False, wtimeout=5000)
        )
        the_activity = db.insert_one(
            {'name': name.lower(),
             'icon': icon}
        )
        return the_activity.inserted_id
    else:
        return the_activity['_id']


def unique_activities(update="false"):
    """get list of activities from the database when update is false, only get those for for future and shared events"""
    activities = []
    ids = {}
    if update == "false":
        events = retrieve_events_from_db(False)
    else:
        events = retrieve_events_from_db(True)
    for event in events:
        new_id = event['activity_id']
        if new_id not in ids.keys():
            ids[new_id] = new_id
            activities.append({'icon': event['activity_icon'], 'name': event['activity_name']})
    return activities
