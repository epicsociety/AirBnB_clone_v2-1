#!/usr/bin/python3
"""Places_reviews module """

from models.place import Place
from models.amenity import Amenity
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from os import getenv


@app_views.route('/places/<place_id>/amenities', strict_slashes=False,
                 methods=['GET'])
def get_amenity_id(place_id):
    """Retrieve amenities related to place_id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    amenity_list = []
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        amenity_objs = place.amenities
    else:
        amenity_objs = place.amenity_ids
    for amenity in amenity_objs:
        amenity_list.append(amenity.to_dict())
    return jsonify(amenity_list)


@app_views.route('places/<place_id>/amenities/<amenity_id',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity_id(place_id, amenity_id):
    """ deletes a amenity related to amenity_id and place_id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        amenity_objs = place.amenities
    else:
        amenity_objs = place.amenity_ids
    if amenity not in amenity_objs:
        abort(404)
    amenity_objs.remove(amenity)
    place.save()
    return jsonify({}), 200


@app_views.route('places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def create_amenity_id(place_id, amenity_id):
    """ Creates a place amenity """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        amenity_objs = place.amenities
    else:
        amenity_objs = place.amenity_ids
    if amenity_id in amenity_objs:
        return 200
    else:
        if getenv('HBNB_TYPE_STORAGE') == 'db':
            for key, value in amenity.items():
                setattr(place.amenities, key, value)
        else:
            place.amenity_ids.append(amenity_id)
    place.save()
    return jsonify(amenity.to_dict()), 201
