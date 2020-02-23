from flask import Blueprint, render_template, request
from datetime import datetime
from what2do2day import app, mongo, csrf
from pymongo import errors, WriteConcern
from urllib.parse import parse_qs

################
#### config ####
################
metrics_bp = Blueprint('metrics_bp', __name__, template_folder='templates', static_folder='static')


##########################
#### helper functions ####
##########################
def load_page(name, pg_type='page', message=False):
    # record a page or layer metric
    try:
        db = mongo.db.metrics_page.with_options(
            write_concern=WriteConcern(w=1, j=False, wtimeout=5000)
        )
        page = {'name': name, 'date': datetime.today(), 'type': pg_type}
        if message:
            page['message'] = message
        result = db.insert_one(page)
        if result is not None:
            pass
        else:
            if app.config['DEBUG']:
                print("failed to insert page metric: ", name)
    except errors.PyMongoError as e:
        # metric db errors are not critical to application running so pass over them
        if app.config['DEBUG']:
            print("failed to insert page metric", e)
        pass


def load_click(link_name, method, pg_name):
    # record a page or layer metric
    try:
        db = mongo.db.metrics_clicks.with_options(
            write_concern=WriteConcern(w=1, j=False, wtimeout=5000)
        )
        click = {'link_name': link_name, 'date': datetime.today(), 'page': pg_name, 'method': method}
        result = db.insert_one(click)
        if result is not None:
            pass
        else:
            if app.config['DEBUG']:
                print("failed to insert click metric: ", link_name)

    except errors.PyMongoError as e:
        # metric db errors are not critical to application running so pass over them
        if app.config['DEBUG']:
            print("failed to insert click metric: ", e)
        pass


################
#### routes ####
################
@metrics_bp.route('/mertrics/', methods=['GET', 'POST'])
def metrics():
    pages = mongo.db.metrics_page.aggregate([
        {
            '$match': {
                'name': {'$not': {'$size': 0}}
            }
        },
        {'$unwind': "$name"},
        {
            '$group': {
                '_id': {'$toLower': '$name'},
                'count': {'$sum': 1}
            }
        },
        {
            '$match': {
                'count': {'$gte': 2}
            }
        },
        {'$sort': {'count': -1}}
    ])
    clicks = mongo.db.metrics_clicks.aggregate([
        {
            '$match': {
                'link_name': {'$not': {'$size': 0}}
            }
        },
        {'$unwind': "$link_name"},
        {
            '$group': {
                '_id': {'$toLower': '$link_name'},
                'count': {'$sum': 1}
            }
        },
        {
            '$match': {
                'count': {'$gte': 2}
            }
        },
        {'$sort': {'count': -1}}
    ])

    return render_template('metrics.html', pages=pages, clicks=clicks)


@metrics_bp.route('/record_click/', methods=['POST'])
def record_click():
    if request.method == "POST":
        query_string = request.get_data()
        query_string = "".join(chr(x) for x in query_string)
        params = parse_qs(query_string)
        if params['link_name'] and params['page'] and params['method']:
            load_click(params['link_name'][0], params['method'][0], params['page'][0])

    return "pass"


@metrics_bp.route('/record_page/<string:name>/<string:pg_type>/', defaults={'message': None}, methods=['POST'])
@metrics_bp.route('/record_page/<string:name>/<string:pg_type>/<string:message>/', methods=['POST'])
def record_page(name, pg_type, message):
    if name is not None and pg_type is not None:
        if message is None:
            load_page(name, pg_type)
        else:
            load_page(name, pg_type, message)
    return True
