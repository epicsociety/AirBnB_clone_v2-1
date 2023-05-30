#!/usr/bin/python3
"""User module """

from models.user import User
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage


@app_views.route('/users', strict_slashes=False,
                 methods=['GET'])
def get_users():
    """A method to retrieve users """
    users = storage.all(User).values()
    user_dict = [user.to_dict() for user in users]
    return jsonify(user_dict)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """A method to retrieve a User object"""
    my_user = storage.get(User, user_id)
    if my_user is None:
        abort(404)
    return jsonify(my_user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """ deletes a user related to requested user_id """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    else:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """ Creates a user """
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")

    email = data.get("email")
    if not email:
        abort(400, "Missing email")
    password = data.get("password")
    if not password:
        abort(400, "Missing password")
    user = User(**data)
    storage.new(user)
    storage.save()
    user_dict = user.to_dict()
    return jsonify(user_dict), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """ updates a user related to the user_id """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    key_list = ['id', 'created_at', 'updated_at', 'email']
    for key, value in data.items():
        if key in key_list:
            pass
        else:
            setattr(user, key, value)
    user_dict = user.to_dict()
    storage.save()
    return jsonify(user_dict), 200
