import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

''' Use Environment Variables to store sensitive information '''
db_user = os.environ.get("DB_USER")
db_password = os.environ.get("DB_PASS")
print("db_user ", db_user)
print("db_pass ", db_password)
app.config["MONGO_DBNAME"] = 'what2do2day'
app.config[
    "MONGO_URI"] = 'mongodb+srv://' + db_user + ':' + db_password + '@mhavlicfirstcluster-pielp.mongodb.net/what2do2day?retryWrites=true&w=majority?'
app.config["MONGO_SERVER_SELECTION_TIMEOUT_MS"] = '2000'
app.config["MONGO_SOCKET_TIMEOUT_MS"] = '2000'
app.config["MONGO_CONNECT_TIMEOUT_MS"] = '2000'
mongo = PyMongo(app)

countries = [
    "Afghanistan",
    "Albania",
    "Algeria",
    "American Samoa",
    "Andorra",
    "Angola",
    "Anguilla",
    "Antarctica",
    "Antigua and Barbuda",
    "Argentina",
    "Armenia",
    "Aruba",
    "Australia",
    "Austria",
    "Azerbaijan",
    "Bahamas (the)",
    "Bahrain",
    "Bangladesh",
    "Barbados",
    "Belarus",
    "Belgium",
    "Belize",
    "Benin",
    "Bermuda",
    "Bhutan",
    "Bolivia (Plurinational State of)",
    "Bonaire, Sint Eustatius and Saba",
    "Bosnia and Herzegovina",
    "Botswana",
    "Bouvet Island",
    "Brazil",
    "British Indian Ocean Territory (the)",
    "Brunei Darussalam",
    "Bulgaria",
    "Burkina Faso",
    "Burundi",
    "Cabo Verde",
    "Cambodia",
    "Cameroon",
    "Canada",
    "Cayman Islands (the)",
    "Central African Republic (the)",
    "Chad",
    "Chile",
    "China",
    "Christmas Island",
    "Cocos (Keeling) Islands (the)",
    "Colombia",
    "Comoros (the)",
    "Congo (the Democratic Republic of the)",
    "Congo (the)",
    "Cook Islands (the)",
    "Costa Rica",
    "Croatia",
    "Cuba",
    "Curaçao",
    "Cyprus",
    "Czechia",
    "Côte d'Ivoire",
    "Denmark",
    "Djibouti",
    "Dominica",
    "Dominican Republic (the)",
    "Ecuador",
    "Egypt",
    "El Salvador",
    "Equatorial Guinea",
    "Eritrea",
    "Estonia",
    "Eswatini",
    "Ethiopia",
    "Falkland Islands (the) [Malvinas]",
    "Faroe Islands (the)",
    "Fiji",
    "Finland",
    "France",
    "French Guiana",
    "French Polynesia",
    "French Southern Territories (the)",
    "Gabon",
    "Gambia (the)",
    "Georgia",
    "Germany",
    "Ghana",
    "Gibraltar",
    "Greece",
    "Greenland",
    "Grenada",
    "Guadeloupe",
    "Guam",
    "Guatemala",
    "Guernsey",
    "Guinea",
    "Guinea-Bissau",
    "Guyana",
    "Haiti",
    "Heard Island and McDonald Islands",
    "Holy See (the)",
    "Honduras",
    "Hong Kong",
    "Hungary",
    "Iceland",
    "India",
    "Indonesia",
    "Iran (Islamic Republic of)",
    "Iraq",
    "Ireland",
    "Isle of Man",
    "Israel",
    "Italy",
    "Jamaica",
    "Japan",
    "Jersey",
    "Jordan",
    "Kazakhstan",
    "Kenya",
    "Kiribati",
    "Korea (the Democratic People's Republic of)",
    "Korea (the Republic of)",
    "Kuwait",
    "Kyrgyzstan",
    "Lao People's Democratic Republic (the)",
    "Latvia",
    "Lebanon",
    "Lesotho",
    "Liberia",
    "Libya",
    "Liechtenstein",
    "Lithuania",
    "Luxembourg",
    "Macao",
    "Madagascar",
    "Malawi",
    "Malaysia",
    "Maldives",
    "Mali",
    "Malta",
    "Marshall Islands (the)",
    "Martinique",
    "Mauritania",
    "Mauritius",
    "Mayotte",
    "Mexico",
    "Micronesia (Federated States of)",
    "Moldova (the Republic of)",
    "Monaco",
    "Mongolia",
    "Montenegro",
    "Montserrat",
    "Morocco",
    "Mozambique",
    "Myanmar",
    "Namibia",
    "Nauru",
    "Nepal",
    "Netherlands (the)",
    "New Caledonia",
    "New Zealand",
    "Nicaragua",
    "Niger (the)",
    "Nigeria",
    "Niue",
    "Norfolk Island",
    "Northern Mariana Islands (the)",
    "Norway",
    "Oman",
    "Pakistan",
    "Palau",
    "Palestine, State of",
    "Panama",
    "Papua New Guinea",
    "Paraguay",
    "Peru",
    "Philippines (the)",
    "Pitcairn",
    "Poland",
    "Portugal",
    "Puerto Rico",
    "Qatar",
    "Republic of North Macedonia",
    "Romania",
    "Russian Federation (the)",
    "Rwanda",
    "Réunion",
    "Saint Barthélemy",
    "Saint Helena, Ascension and Tristan da Cunha",
    "Saint Kitts and Nevis",
    "Saint Lucia",
    "Saint Martin (French part)",
    "Saint Pierre and Miquelon",
    "Saint Vincent and the Grenadines",
    "Samoa",
    "San Marino",
    "Sao Tome and Principe",
    "Saudi Arabia",
    "Senegal",
    "Serbia",
    "Seychelles",
    "Sierra Leone",
    "Singapore",
    "Sint Maarten (Dutch part)",
    "Slovakia",
    "Slovenia",
    "Solomon Islands",
    "Somalia",
    "South Africa",
    "South Georgia and the South Sandwich Islands",
    "South Sudan",
    "Spain",
    "Sri Lanka",
    "Sudan (the)",
    "Suriname",
    "Svalbard and Jan Mayen",
    "Sweden",
    "Switzerland",
    "Syrian Arab Republic",
    "Taiwan (Province of China)",
    "Tajikistan",
    "Tanzania, United Republic of",
    "Thailand",
    "Timor-Leste",
    "Togo",
    "Tokelau",
    "Tonga",
    "Trinidad and Tobago",
    "Tunisia",
    "Turkey",
    "Turkmenistan",
    "Turks and Caicos Islands (the)",
    "Tuvalu",
    "Uganda",
    "Ukraine",
    "United Arab Emirates (the)",
    "United Kingdom of Great Britain and Northern Ireland (the)",
    "United States Minor Outlying Islands (the)",
    "United States of America (the)",
    "Uruguay",
    "Uzbekistan",
    "Vanuatu",
    "Venezuela (Bolivarian Republic of)",
    "Viet Nam",
    "Virgin Islands (British)",
    "Virgin Islands (U.S.)",
    "Wallis and Futuna",
    "Western Sahara",
    "Yemen",
    "Zambia",
    "Zimbabwe",
    "Åland Islands"
];


def db_issue(e):
    print("mongo.db.client.server_info(): " + mongo.db.client_info() + "error" + e)


@app.route('/')
@app.route('/home')
def home():
    """ initial/default routing for app is the home page """
    return render_template('pages/home.html')


@app.route('/get_events')
def get_events():
    try:
        list_events = mongo.db.events.find()
    except Exception as e:
        db_issue(e)
        list_events = []

    return render_template('pages/events/events.html', events=list_events, filter='none')


@app.route('/filter_events', methods=['POST'])
def filter_events():
    return render_template('pages/events/events.html', events=mongo.db.events.find(), filter='none')


@app.route('/add_event', methods=['GET', 'POST'])
def add_event():
    if request.method == 'POST':
        filters = 'yes'
    else:
        filters = 'none'

    try:
        list_places = mongo.db.places.find()
    except Exception as e:
        db_issue(e)
        list_places = []

    return render_template('pages/events/add_event.html', places=list_places, filter=filters)


@app.route('/get_places')
def get_places():
    try:
        list_places = mongo.db.places.find()
    except Exception as e:
        db_issue(e)
        list_places = []
    return render_template('pages/places/places.html', places=list_places)


@app.route('/add_place')
def add_place():
    try:
        list_activities = mongo.db.activities.find()
    except Exception as e:
        db_issue(e)
        list_activities = []
    return render_template('pages/places/add_place.html', activities=list_activities, countries=countries)


if __name__ == '__main__':
    app.run(host=os.getenv("IP", "0.0.0.0"),
            port=int(os.getenv("PORT", "5000")),
            debug=True)

"""
<!--

Traceback (most recent call last):
  File "/Users/mhavlicek/PycharmProjects/what2do2day/.venv/lib/python3.7/site-packages/flask/app.py", line 2463, in __call__
    return self.wsgi_app(environ, start_response)
  File "/Users/mhavlicek/PycharmProjects/what2do2day/.venv/lib/python3.7/site-packages/flask/app.py", line 2449, in wsgi_app
    response = self.handle_exception(e)
  File "/Users/mhavlicek/PycharmProjects/what2do2day/.venv/lib/python3.7/site-packages/flask/app.py", line 1866, in handle_exception
    reraise(exc_type, exc_value, tb)
  File "/Users/mhavlicek/PycharmProjects/what2do2day/.venv/lib/python3.7/site-packages/flask/_compat.py", line 39, in reraise
    raise value
  File "/Users/mhavlicek/PycharmProjects/what2do2day/.venv/lib/python3.7/site-packages/flask/app.py", line 2446, in wsgi_app
    response = self.full_dispatch_request()
  File "/Users/mhavlicek/PycharmProjects/what2do2day/.venv/lib/python3.7/site-packages/flask/app.py", line 1951, in full_dispatch_request
    rv = self.handle_user_exception(e)
  File "/Users/mhavlicek/PycharmProjects/what2do2day/.venv/lib/python3.7/site-packages/flask/app.py", line 1820, in handle_user_exception
    reraise(exc_type, exc_value, tb)
  File "/Users/mhavlicek/PycharmProjects/what2do2day/.venv/lib/python3.7/site-packages/flask/_compat.py", line 39, in reraise
    raise value
  File "/Users/mhavlicek/PycharmProjects/what2do2day/.venv/lib/python3.7/site-packages/flask/app.py", line 1949, in full_dispatch_request
    rv = self.dispatch_request()
  File "/Users/mhavlicek/PycharmProjects/what2do2day/.venv/lib/python3.7/site-packages/flask/app.py", line 1935, in dispatch_request
    return self.view_functions[rule.endpoint](**req.view_args)
  File "/Users/mhavlicek/PycharmProjects/what2do2day/app.py", line 37, in get_events
    return render_template('pages/events/events.html', events=list_events, filter='none')
  File "/Users/mhavlicek/PycharmProjects/what2do2day/.venv/lib/python3.7/site-packages/flask/templating.py", line 140, in render_template
    ctx.app,
  File "/Users/mhavlicek/PycharmProjects/what2do2day/.venv/lib/python3.7/site-packages/flask/templating.py", line 120, in _render
    rv = template.render(context)
  File "/Users/mhavlicek/PycharmProjects/what2do2day/.venv/lib/python3.7/site-packages/jinja2/asyncsupport.py", line 76, in render
    return original_render(self, *args, **kwargs)
  File "/Users/mhavlicek/PycharmProjects/what2do2day/.venv/lib/python3.7/site-packages/jinja2/environment.py", line 1008, in render
    return self.environment.handle_exception(exc_info, True)
  File "/Users/mhavlicek/PycharmProjects/what2do2day/.venv/lib/python3.7/site-packages/jinja2/environment.py", line 780, in handle_exception
    reraise(exc_type, exc_value, tb)
  File "/Users/mhavlicek/PycharmProjects/what2do2day/.venv/lib/python3.7/site-packages/jinja2/_compat.py", line 37, in reraise
    raise value.with_traceback(tb)
  File "/Users/mhavlicek/PycharmProjects/what2do2day/templates/pages/events/events.html", line 1, in top-level template code
    {% extends 'pages/base.html' %}
  File "/Users/mhavlicek/PycharmProjects/what2do2day/.venv/lib/python3.7/site-packages/jinja2/environment.py", line 1005, in render
    return concat(self.root_render_func(self.new_context(vars)))
  File "/Users/mhavlicek/PycharmProjects/what2do2day/templates/pages/events/events.html", line 14, in root
    </p>
  File "/Users/mhavlicek/PycharmProjects/what2do2day/templates/pages/base.html", line 16, in root
    
  File "/Users/mhavlicek/PycharmProjects/what2do2day/templates/pages/events/events.html", line 24, in block_content
    </p>
  File "/Users/mhavlicek/PycharmProjects/what2do2day/.venv/lib/python3.7/site-packages/pymongo/cursor.py", line 787, in count
    cmd, self.__collation, session=self.__session)
  File "/Users/mhavlicek/PycharmProjects/what2do2day/.venv/lib/python3.7/site-packages/pymongo/collection.py", line 1600, in _count
    _cmd, self._read_preference_for(session), session)
  File "/Users/mhavlicek/PycharmProjects/what2do2day/.venv/lib/python3.7/site-packages/pymongo/mongo_client.py", line 1454, in _retryable_read
    read_pref, session, address=address)
  File "/Users/mhavlicek/PycharmProjects/what2do2day/.venv/lib/python3.7/site-packages/pymongo/mongo_client.py", line 1253, in _select_server
    server = topology.select_server(server_selector)
  File "/Users/mhavlicek/PycharmProjects/what2do2day/.venv/lib/python3.7/site-packages/pymongo/topology.py", line 235, in select_server
    address))
  File "/Users/mhavlicek/PycharmProjects/what2do2day/.venv/lib/python3.7/site-packages/pymongo/topology.py", line 193, in select_servers
    selector, server_timeout, address)
  File "/Users/mhavlicek/PycharmProjects/what2do2day/.venv/lib/python3.7/site-packages/pymongo/topology.py", line 209, in _select_servers_loop
    self._error_message(selector))
pymongo.errors.ServerSelectionTimeoutError: mhavlicfirstcluster-shard-00-02-pielp.mongodb.net:27017: timed out,mhavlicfirstcluster-shard-00-01-pielp.mongodb.net:27017: [Errno 61] Connection refused,mhavlicfirstcluster-shard-00-00-pielp.mongodb.net:27017: timed out

-->

"""
