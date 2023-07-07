from flask import Blueprint, jsonify, request
from app.models.user import User

bp = Blueprint('users', __name__)


@bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    result = User.get(user_id)
    if result:
        user = {
            'id': result.user_id,
            'name': result.name,
            'email': result.email
        }
        return jsonify(user), 200
    return jsonify({'message': 'User not found'}), 404


@bp.route('/', methods=['GET'])
def get_users():
    results = User.get_all()
    users = []
    for result in results:
        user = {
            'id': result.user_id,
            'name': result.name,
            'email': result.email
        }
        users.append(user)
    return jsonify(users), 200


@bp.route('/', methods=['POST'])
def create_user():
    data = request.get_json()
    params = (data['id'], data['name'], data['email'], data['password'])
    User.create(*params)
    return jsonify({'message': 'User created successfully'}), 200


@bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    msg = User.delete(user_id)
    if msg is None:
        return jsonify({'message': 'User deleted successfully'}), 200
    else:
        return jsonify({'message': msg}), 200

