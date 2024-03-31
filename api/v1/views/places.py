#!/usr/bin/python3
"""Creates views for Place objects that handles all default RESTFul API action
"""

from api.v1.views.index import app_views
from flask import jsonify, abort, request, make_response

from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'])
def places_in_city(city_id):
    """Retrieves a Place object
    """
    if request.method == 'GET':
        city = storage.get(City, city_id)
        if city is None:
            abort(404)

        places = city.places
        places_list = []
        for place in places:
            places_list.append(place.to_dict())
        return jsonify(places_list)

    if request.method == 'POST':
        city = storage.get(City, city_id)
        if city is None:
            abort(404)

        place = request.get_json()
        if place is None:
            abort(400, description="Not a JSON")
        elif 'user_id' not in place:
            abort(400, description="Missing user_id")
        elif 'name' not in place:
            abort(400, description="Missing name")

        user_id = request.get_json().get('user_id')
        if storage.get(User, user_id) is None:
            abort(404)

        new_place = Place(**place)
        new_place.city_id = city_id
        new_place.user_id = user_id

        new_place.save()
        return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['GET'])
def places(place_id):
    """Retrieves the list of a place objects
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    return make_response(jsonify(place.to_dict()), 200)


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """Deletes a Place object
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """Updates a Place object
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    place_data = request.get_json()
    if place_data is None:
        abort(400, description="Not a JSON")

    for key, value in place_data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)

    place.save()
    return make_response(jsonify(place.to_dict()), 200)

