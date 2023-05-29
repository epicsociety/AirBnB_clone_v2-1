#!/usr/bin/python3
"""Amenity module """

from models.amenity import Amenity
from models.city import City
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage


@app_views.route('/amenities', strict_slashes=False,
                 methods=['GET'])
def get_amenities():
    """A method to retrieve amenities """
    amenities = storage.all(Amenity).values()
    amenity_list = [amenity.to_dict() for amenity in amenities]
    return amenity_list

@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    """A method to retrieve an Amenity object"""
    my_amenity = storage.get(Amenity, amenity_id)
    if my_amenity is None:
        abort(404)
    return jsonify(my_amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """ deletes an amenity related to requested amenity_id """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    else:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'])
def create_amenity():
    """ Creates an amenity """
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    # key = request.keys()
    name = data.get("name")
    if not name:
        abort(400, "Missing name")
    amenity = Amenity(name=name)
    amenity_dict = amenity.to_dict()
    storage.new(amenity)
    storage.save()
    return jsonify(amemity_dict), 201

@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """ updates an amenity related to the amenity_id """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    for key, value in data.items():
        if key == 'id' or key == 'created_at' or key == 'updated_at':
            pass
        else:
            setattr(amenity, key, value)
    amenity_dict = amenity.to_dict()
    storage.save()
    return jsonify(amenity_dict), 200    
