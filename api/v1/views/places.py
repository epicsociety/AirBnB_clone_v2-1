#!/usr/bin/python3
"""City module """

from models.place import Place
from models.city import City
from models.user import User
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['GET'])
def get_places(city_id):
    """A method to retrieve places """
    cities = storage.get(City, city_id)
    if cities is None:
        abort(404)
    places = [place.to_dict() for place in cities.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """A method to retrieve a place object"""
    my_place = storage.get(Place, place_id)
    if my_place is None:
        abort(404)
    return jsonify(my_place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """ deletes a place related to requested place_id """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    else:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """ Creates a place """
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    user_id = data.get("user_id")
    if not user_id:
        abort(400, "Missing user_id")
    user_values = storage.all(User).values()
    if user_id not in user_values:
        abort(404)
    name = data.get("name")
    if not name:
        abort(400, "Missing name")
    place = Place(**data)
    storage.new(place)
    storage.save()
    place_dict = place.to_dict()
    return jsonify(place_dict), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ updates a place related to the place_id """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    key_list = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key in key_list:
            pass
        else:
            setattr(place, key, value)
    place_dict = place.to_dict()
    storage.save()
    return jsonify(place_dict), 200
