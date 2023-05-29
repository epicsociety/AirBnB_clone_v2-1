#!/usr/bin/python3
""" view for State objects """

from models.state import State
from models import storage
from flask import jsonify, request
from api.v1.views import app_views

@app_views.route('/states', strict_slashes=False, methods=['GET'])
def get_states():
    """ retrieves all states objects """
    states = storage.all(State).values()
    state_list = [state.to_dict() for state in states]
    return jsonify(state_list)
