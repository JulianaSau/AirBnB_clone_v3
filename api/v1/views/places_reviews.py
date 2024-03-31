#!/usr/bin/python3
"""Creates views for Place objects that handles all default RESTFul API action
"""

from api.v1.views.index import app_views
from flask import jsonify, abort, request, make_response

from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'])
def reviews_in_place(place_id):
    """Retrieves a Review object
    """
    if request.method == 'GET':
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)

        reviews = place.reviews
        reviews_list = []
        for review in reviews:
            reviews_list.append(review.to_dict())
        return jsonify(reviews_list)

    if request.method == 'POST':
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)

        review = request.get_json()
        if review is None:
            abort(400, description="Not a JSON")
        elif 'user_id' not in review:
            abort(400, description="Missing user_id")
        elif 'text' not in review:
            abort(400, description="Missing text")

        user_id = request.get_json().get('user_id')
        if storage.get(User, user_id) is None:
            abort(404)

        new_review = Review(**review)
        new_review.place_id = place_id
        new_review.user_id = user_id

        new_review.save()
        return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def review(review_id):
    """Retrieves the list of a place objects
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    return make_response(jsonify(review.to_dict()), 200)


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """Deletes a Review object
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """Updates a Place object
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    review_data = request.get_json()
    if review_data is None:
        abort(400, description="Not a JSON")

    for key, value in review_data.items():
        if key not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(review, key, value)

    review.save()
    return make_response(jsonify(review.to_dict()), 200)

