from flask import Blueprint, Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo

from app import mongo

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_user = Blueprint('user', __name__, url_prefix='/user')


@mod_user.route('/user/<email>', methods=['GET', 'POST'])
def user(email):
    the_user = mongo.db.users.find_one({'email': email.lower()})
    if the_user is None:
        the_user_id = mongo.db.users.insert_one(email.lower())
    else:
        the_user_id = the_user['_id']
    return the_user_id
