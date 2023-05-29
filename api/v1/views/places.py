#!/usr/bin/python3
"""City module """

from models.place import Place
from models.city import City
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['GET'])
def get_places(city_id):
    """A method to retrieve places """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in cities.places]
    return places

@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """A method to retrieve a place object"""
    my_place = storage.get(Place, place_id)
    if my_place is None:
        abort(404)
    return jsonify(my_place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """ deletes a place related to requested place_id """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    else:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """ Creates a place """
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    # key = request.keys()
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    user_values = storage.all(User).values()
    if city_id not in user_values:
        abort(404)
    user_id = data.get("user_id")
    if not user_id:
        abort(400, "Missing user_id")
    name = data.get("name")
    if not name:
        abort(400, "Missing name")
    place = Place(name=name, city_id=city_id, user_id=user_id)
    place_dict = place.to_dict()
    storage.new(place)
    storage.save()
    return jsonify(place_dict), 201

@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """ updates a place related to the place_id """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    for key, value in data.items():
        if key == 'id' or key == 'created_at' or key == 'updated_at':
            pass
        else:
            setattr(place, key, value)
    place_dict = place.to_dict()
    storage.save()
    return jsonify(place_dict), 200    
