from flask import Blueprint, jsonify, request
from app.models.location import Location

bp = Blueprint('locations', __name__)


@bp.route('/<string:location_name>', methods=['GET'])
def get_location(location_name: str):
    result = Location.get(location_name)
    if result:
        location = {
            'location_name': result.location_name,
            'latitude': result.latitude,
            'longitude': result.longitude,
            'patrol_division': result.patrol_division
        }
        return jsonify(location), 200
    return jsonify({'message': 'Location not found'}), 404


@bp.route('/', methods=['GET'])
def get_locations():
    results = Location.get_all()
    locations = []
    for result in results:
        location = {
            'location_name': result.location_name,
            'latitude': result.latitude,
            'longitude': result.longitude,
            'patrol_division': result.patrol_division
        }
        locations.append(location)
    return jsonify(locations), 200


@bp.route('/', methods=['POST'])
def create_location():
    data = request.get_json()
    params = (data['location_name'], data['latitude'], data['longitude'],
              data['patrol_division'])
    Location.create(*params)
    return jsonify({'message': 'Location created successfully'}), 200


@bp.route('/<string:location_name>', methods=['DELETE'])
def delete_location(location_name):
    msg = Location.delete(location_name)
    if msg is None:
        return jsonify({'message': 'Location deleted successfully'}), 200
    else:
        return jsonify({'message': msg}), 200


