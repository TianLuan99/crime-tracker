from flask import Blueprint, jsonify, request
from app.models.crime_type import CrimeType

bp = Blueprint('crime_types', __name__)


@bp.route('/<int:type_code>', methods=['GET'])
def get_crime_type(type_code: int):
    result = CrimeType.get(type_code)
    if result:
        crime_type = {
            'type_code': result.type_code,
            'description': result.description
        }
        return jsonify(crime_type), 200
    return jsonify({'message': 'Crime type not found'}), 404


@bp.route('/', methods=['GET'])
def get_crime_types():
    results = CrimeType.get_all()
    crime_types = []
    for result in results:
        crime_type = {
            'type_code': result.type_code,
            'description': result.description
        }
        crime_types.append(crime_type)
    return jsonify(crime_types), 200


@bp.route('/', methods=['POST'])
def create_crime_type():
    data = request.get_json()
    params = (data['type_code'], data['description'])
    CrimeType.create(*params)
    return jsonify({'message': 'Crime type created successfully'}), 200


@bp.route('/<int:type_code>', methods=['DELETE'])
def delete_crime_type(type_code: int):
    msg = CrimeType.delete(type_code)
    if msg is None:
        return jsonify({'message': 'Crime type deleted successfully'}), 200
    else:
        return jsonify({'message': msg}), 200

