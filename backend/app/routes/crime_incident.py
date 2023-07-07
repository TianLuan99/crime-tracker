from flask import Blueprint, jsonify, request
from app.models.crime_incident import CrimeIncident

bp = Blueprint('crime_incidents', __name__)


@bp.route('/query', methods=['POST'])
def query():
    data = request.get_json()
    location_name = data.get('location_name', None)
    date = data.get('date', None)
    time = data.get('time', None)
    status = data.get('status', None)
    if not (location_name or date or time or status):
        return jsonify({'message': 'No parameter provided'}), 403
    results = CrimeIncident.search(location_name, date, time, status)
    crime_incidents = []
    for result in results:
        crime_incident = {
            'incident_id': result.incident_id,
            'location_name': result.location_name,
            'date': result.date,
            'time': str(result.time),
            'status': result.status
        }
        crime_incidents.append(crime_incident)
    return jsonify(crime_incidents), 200


@bp.route('/', methods=['POST'])
def create_crime_incident():
    data = request.get_json()
    params = (data['location_name'], data['date'], data['time'],
              data['status'])
    try:
        CrimeIncident.create(*params)
        return jsonify({'message': 'Crime incident created successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400


@bp.route('/<int:incident_id>', methods=['PUT'])
def update_crime_incident(incident_id):
    data = request.get_json()
    params = (incident_id, data['date'], data['time'], data['status'])
    try:
        CrimeIncident.update(*params)
        return jsonify({'message': 'Crime incident updated successfully'}), 200
    except Exception as e:
        print(e)
        return jsonify({'message': str(e)}), 400


@bp.route('/<int:incident_id>', methods=['GET'])
def get_crime_incident(incident_id):
    result = CrimeIncident.get(incident_id)
    if result:
        crime_incident = {
            'incident_id': result.incident_id,
            'location_name': result.location_name,
            'date': result.date,
            'time': str(result.time),
            'status': result.status
        }
        return jsonify(crime_incident), 200
    return jsonify({'message': 'Crime incident not found'}), 404


@bp.route('/', methods=['GET'])
def get_crime_incidents():
    results = CrimeIncident.get_all()
    crime_incidents = []
    for result in results:
        crime_incident = {
            'incident_id': result.incident_id,
            'location_name': result.location_name,
            'date': result.date,
            'time': str(result.time),
            'status': result.status
        }
        crime_incidents.append(crime_incident)
    return jsonify(crime_incidents), 200


@bp.route('/<int:incident_id>', methods=['DELETE'])
def delete_crime_incident(incident_id):
    msg = CrimeIncident.delete(incident_id)
    if msg is None:
        return jsonify({'message': 'Crime incident deleted successfully'}), 200
    else:
        return jsonify({'message': msg}), 404
