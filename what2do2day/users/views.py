from flask import Blueprint
from pymongo import WriteConcern
from what2do2day import mongo

################
#### config ####
################
users_bp = Blueprint('users_bp', __name__, template_folder='templates', static_folder='static')


##########################
#### helper functions ####
##########################
def get_add_user_id(email):
    """retrieve or create a user based on email"""
    the_user = mongo.db.users.find_one({'email': email.lower()})
    if the_user is None:
        db = mongo.db.users.with_options(
            # for production application, we'd want a majority(or 2) value and True for confirmation on writing the data
            write_concern=WriteConcern(w=1, j=False, wtimeout=5000)
        )
        the_user = db.insert_one(
            {'email': email.lower()}
        )
        return the_user.inserted_id
    else:
        return the_user['_id']

################
#### routes ####
################
