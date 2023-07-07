from flask import Flask
from app.routes import users, query, locations, crime_types, crime_report, crime_incident
from flask_cors import CORS

app = Flask(__name__)

app.register_blueprint(users.bp, url_prefix='/user')
app.register_blueprint(query.bp, url_prefix='/query')
app.register_blueprint(locations.bp, url_prefix='/location')
app.register_blueprint(crime_types.bp, url_prefix='/crime-type')
app.register_blueprint(crime_report.bp, url_prefix='/crime-report')
app.register_blueprint(crime_incident.bp, url_prefix='/crime-incident')

CORS(app, resources={r'*': {'origins': '*'}})

app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/')
def index():
    print("Hello")
    return 'Welcome to Crime Tracker backend API'
