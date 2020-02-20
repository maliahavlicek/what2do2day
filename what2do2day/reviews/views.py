
from flask import render_template, Blueprint
from flask import current_app as app
from bson.objectid import ObjectId

from pymongo import WriteConcern
from datetime import datetime, timedelta

from what2do2day import mongo
from what2do2day.reviews.forms import ReviewForm
from what2do2day.users.views import get_add_user_id

################
#### config ####
################

reviews_bp = Blueprint('reviews_bp', __name__, template_folder='templates', static_folder='static')

##########################
#### helper functions ####
##########################
def db_add_review(review):
    """"need to make sure insert rating as an integer"""
    db = mongo.db.reviews.with_options(
        write_concern=WriteConcern(w=1, j=False, wtimeout=5000)
    )
    the_review = db.insert_one(review)
    return the_review.inserted_id


################
#### routes ####
################

@reviews_bp.route('/add_review/<string:place_id>/', methods=['GET', 'POST'])
def add_review(place_id):
    form = ReviewForm()
    form.use_place_email.data = "n"
    show_modal = False

    the_place = mongo.db.places.find_one({'_id': ObjectId(place_id)})
    if the_place is not None:
        place_name = the_place['name']
    else:
        return render_template('error.html', reason="I couldn't find the place you were looking for.")

    if form.validate_on_submit():
        review = {'place': ObjectId(place_id), 'date': datetime.today(),
                  'rating': int(form.data['rating']),
                  'comments': form.data['comments'].strip(),
                  'share': form.share.data}

        email = form.author.data.strip().lower()
        review['user'] = get_add_user_id(email)

        # check if user has added a review for this place in the last 7 days (want to make it harder to bloat reviews)
        one_week_ago = datetime.today() - timedelta(days=7)
        too_recent = mongo.db.reviews.find_one({"date": {"$gte": one_week_ago}, "user": review['user']})
        if too_recent is not None:
            show_modal = {
                'status': "ERROR",
                'message': "Sorry, it looks like you have already submitted a review within the last week."
            }
        else:
            show_modal = {
                'status': "OK",
                'message': "Thank you for adding to the community! It may take up to 5 minutes before your review shows up."
            }
            review_id = db_add_review(review)

    return render_template('add_review.html', id=place_id, name=place_name, form=form, show_modal=show_modal)
