#!/usr/bin/python3
"""City module """

from models.state import State
from models.city import City
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['GET'])
def get_cities(state_id):
    """A method to retrieve cities """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    """A method to retrieve a City object"""
    my_city = storage.get(City, city_id)
    if my_city is None:
        abort(404)
    return jsonify(my_city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """ deletes a city related to requested city_id """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    else:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    """ Creates a city """
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    # key = request.keys()
    name = data.get("name")
    if not name:
        abort(400, "Missing name")
    city = City(name=name, state_id=state_id)
    city_dict = city.to_dict()
    storage.new(city)
    storage.save()
    return jsonify(city_dict), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """ updates a city related to the city_id """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    for key, value in data.items():
        if key == 'id' or key == 'created_at' or key == 'updated_at':
            pass
        else:
            setattr(city, key, value)
    city_dict = city.to_dict()
    storage.save()
    return jsonify(city_dict), 200
