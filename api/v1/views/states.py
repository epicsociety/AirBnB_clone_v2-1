#!/usr/bin/python3
""" view for State objects """

from models.state import State
from models import storage
from flask import abort, request
from api.v1.views import app_views


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def get_states():
    """ retrieves all states objects """
    states = storage.all(State).values()
    state_list = [state.to_dict() for state in states]
    return state_list


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state_id(state_id):
    """ retrieves states according state_id"""
    my_state = storage.get(State, state_id)
    if my_state is None:
        abort(404)
    return my_state.to_dict()


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """ deletes a state related to requested state_id """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    else:
        storage.delete(state)
        return {}, 200


@app_views.route('/states', methods=['POST'])
def create_state():
    """ Create a state """
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    # key = request.keys()
    name = data.get("name")
    if not name:
        abort(400, "Missing name")
    state = State(name=name)
    state.save()
    return state.to_dict(), 201
