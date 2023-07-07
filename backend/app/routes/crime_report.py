from flask import Blueprint, jsonify, request
from app.models.crime_report import CrimeReport

bp = Blueprint('crime_reports', __name__)


@bp.route('/query', methods=['POST'])
def query():
    data = request.get_json()
    weapon = data.get('weapon', None)
    premise = data.get('premise', None)
    victim_age = data.get('victim_age', None)
    victim_sex = data.get('victim_sex', None)
    victim_descent = data.get('victim_descent', None)
    if not (weapon or premise or victim_age or victim_sex or victim_descent):
        return jsonify({'message': 'No parameter provided'}), 403
    # print("Searching...")
    results = CrimeReport.search(weapon, premise, victim_age, victim_sex,
                                 victim_descent)
    crime_reports = []
    for result in results:
        crime_report = {
            'report_id': result.report_id,
            'user_id': result.user_id,
            'incident_id': result.incident_id,
            'date': result.date,
            'weapon': result.weapon,
            'premise': result.premise,
            'victim_age': result.victim_age,
            'victim_sex': result.victim_sex,
            'victim_descent': result.victim_descent
        }
        crime_reports.append(crime_report)
    return jsonify(crime_reports), 200


@bp.route('/<int:incident_id>/<int:user_id>/<int:report_id>', methods=['GET'])
def get_crime_report(incident_id: int, user_id: int, report_id: int):
    result = CrimeReport.get(incident_id, user_id, report_id)
    if result:
        crime_report = {
            'report_id': result.report_id,
            'user_id': result.user_id,
            'incident_id': result.incident_id,
            'date': result.date,
            'weapon': result.weapon,
            'premise': result.premise,
            'victim_age': result.victim_age,
            'victim_sex': result.victim_sex,
            'victim_descent': result.victim_descent
        }
        return jsonify(crime_report), 200
    return jsonify({'message': 'Crime report not found'}), 404


@bp.route('/', methods=['GET'])
def get_crime_reports():
    results = CrimeReport.get_all()
    crime_reports = []
    for result in results:
        crime_report = {
            'report_id': result.report_id,
            'user_id': result.user_id,
            'incident_id': result.incident_id,
            'date': result.date,
            'weapon': result.weapon,
            'premise': result.premise,
            'victim_age': result.victim_age,
            'victim_sex': result.victim_sex,
            'victim_descent': result.victim_descent
        }
        crime_reports.append(crime_report)
    return jsonify(crime_reports), 200


@bp.route('/', methods=['POST'])
def create_crime_report():
    data = request.get_json()
    # current user id is always 0, should be changed to real user id in future
    params = (0, data['incident_id'], data['date'], data['weapon'],
              data['premise'], data['victim_age'], data['victim_sex'],
              data['victim_descent'])
    CrimeReport.create(*params)
    return jsonify({'message': 'Crime report created successfully'}), 200


@bp.route('/<int:incident_id>/<int:user_id>/<int:report_id>',
          methods=['DELETE'])
def delete_crime_report(incident_id: int, user_id: int, report_id: int):
    msg = CrimeReport.delete(incident_id, user_id, report_id)
    if msg is None:
        return jsonify({'message': 'Crime report deleted successfully'}), 200
    else:
        return jsonify({'message': msg}), 404


@bp.route('/<int:incident_id>/<int:user_id>/<int:report_id>', methods=['PUT'])
def update_crime_report(incident_id: int, user_id: int, report_id: int):
    data = request.get_json()
    weapon = data.get('weapon', None)
    premise = data.get('victim_descent', None)
    victim_age = data.get('victim_age', None)
    victim_sex = data.get('victim_sex', None)
    victim_descent = data.get('victim_descent', None)
    if not (weapon or premise or victim_age or victim_sex or victim_descent):
        return jsonify({'message': 'No parameter provided'}), 403
    msg = CrimeReport.update(incident_id, user_id, report_id, weapon, premise,
                             victim_age, victim_sex, victim_descent)
    if msg is None:
        return jsonify({'message': 'Crime report updated successfully'}), 200
    else:
        return jsonify({'message': msg}), 404


@bp.route('/<int:incident_id>/', methods=['GET'])
def get_crime_reports_by_incident(incident_id: int):
    results = CrimeReport.get_all_by_incident(incident_id)
    crime_reports = []
    for result in results:
        crime_report = {
            'report_id': result.report_id,
            'user_id': result.user_id,
            'incident_id': result.incident_id,
            'date': result.date,
            'weapon': result.weapon,
            'premise': result.premise,
            'victim_age': result.victim_age,
            'victim_sex': result.victim_sex,
            'victim_descent': result.victim_descent
        }
        crime_reports.append(crime_report)
    return jsonify(crime_reports), 200
