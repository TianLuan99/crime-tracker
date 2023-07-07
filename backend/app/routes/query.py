from flask import Blueprint, jsonify, request
from app.models.queries import \
    get_feamle_crime_count_by_victim_descent_in_Central_Southwest, \
    get_crime_stats, \
    generate_crime_report

bp = Blueprint('queries', __name__)


@bp.route('/female-crime-descent-count', methods=['GET'])
def get_crime_count():
    result = get_feamle_crime_count_by_victim_descent_in_Central_Southwest()
    if result:
        response = []
        for row in result:
            response.append({'Descent': row[0], 'Crime_Count': row[1]})
        return jsonify(response), 200
    return jsonify({'message': 'No results found'}), 404


@bp.route('/crime_stats', methods=['GET'])
def crime_stats():
    results = get_crime_stats()
    if results:
        response = []
        for row in results:
            response.append({'Patrol_Division': row[0], 'Crime_Count': row[1]})
        return jsonify(response), 200
    return jsonify({'message': 'No results found'}), 404


@bp.route('/generate_report', methods=['POST'])
def crime_report():
    request_data = request.get_json()
    start_date = request_data.get('start_date', None)
    end_date = request_data.get('end_date', None)
    if not start_date or not end_date:
        return jsonify({'message':
                        'start_date and end_date are required'}), 400
    results = generate_crime_report(start_date, end_date)
    # print(results)
    if results:
        return jsonify(results), 200
    return jsonify({'message': 'No results found'}), 404
