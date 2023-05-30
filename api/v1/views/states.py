#!/usr/bin/python3
""" view for State objects """

from models.state import State
from models import storage
from flask import abort, request, jsonify, make_response
from api.v1.views import app_views


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def get_states():
    """ retrieves all states objects """
    states = storage.all(State).values()
    state_list = [state.to_dict() for state in states]
    return jsonify(state_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_id(state_id):
    """ retrieves states according state_id"""
    my_state = storage.get(State, state_id)
    if my_state is None:
        abort(404)
    return jsonify(my_state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """ deletes a state related to requested state_id """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    else:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
   """ Create a state """
   data = request.get_json()
   if not data:
       abort(400, "Not a JSON")
   if "name" not in data:
       abort(400, "Missing name")
   state = State(**data)
   storage.new(state)
   storage.save()
   state_dict = state.to_dict()
   return make_response(jsonify(state_dict), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """ updates a state related to the state_id """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    for key, value in data.items():
        if key == 'id' or key == 'created_at' or key == 'updated_at':
            pass
        else:
            setattr(state, key, value)
    state_dict = state.to_dict()
    storage.save()
    return jsonify(state_dict), 200
