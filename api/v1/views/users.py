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
    return user_dict

@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """A method to retrieve a User object"""
    my_user = storage.get(User, user_id)
    if my_user is None:
        abort(404)
    return jsonify(my_user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """ deletes a user related to requested user_id """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    else:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200


@app_views.route('/users', methods=['POST'])
def create_user():
    """ Creates a user """
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    # key = request.keys()
    email = data.get("email")
    if not email:
        abort(400, "Missing email")
    password = data.get("password")
    if not password:
        abort(400, "Missing password")
    user = User(email=email, password=password)
    user_dict = user.to_dict()
    storage.new(user)
    storage.save()
    return jsonify(user_dict), 201

@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """ updates a user related to the user_id """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    for key, value in data.items():
        if key == 'id' or key == 'created_at' or key == 'updated_at':
            pass
        else:
            setattr(user, key, value)
    user_dict = user.to_dict()
    storage.save()
    return jsonify(user_dict), 200    
