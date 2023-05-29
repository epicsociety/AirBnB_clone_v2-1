#!/usr/bin/python3
"""Places_reviews module """

from models.place import Place
from models.review import Review
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['GET'])
def get_reviews(place_id):
    """A method to retrieve reviews """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = [review.to_dict() for review in places.reviews]
    return reviews

@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    """A method to retrieve a Review object"""
    my_review = storage.get(Review, review_id)
    if my_review is None:
        abort(404)
    return jsonify(my_review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """ deletes a review related to requested review_id """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    else:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    """ Creates a review """
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    # key = request.keys()
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    user_id = data.get("user_id")
    if not user_id:
        abort(400, "Missing user_id")

    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    text = data.get("text")
    if not text:
        abort(400, "Missing text")

    review = Review(text=text, place_id=place_id, user_id=user_id)
    review_dict = review.to_dict()
    storage.new(review)
    storage.save()
    return jsonify(review_dict), 201

@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(city_id):
    """ updates a review related to the review_id """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    my_list = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key in my_list:
            pass
        else:
            setattr(review, key, value)
    review_dict = review.to_dict()
    storage.save()
    return jsonify(review_dict), 200    
