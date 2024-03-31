#!/usr/bin/python3
"""Creates views for State objects that handles all default RESTFul API action
"""

from api.v1.views.index import app_views
from flask import jsonify, abort, request, make_response

from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'])
def cities_in_state(state_id):
    """Retrieves a State object
    """
    if request.method == 'GET':
        state = storage.get(State, state_id)
        if state is None:
            abort(404)

        cities = state.cities
        cities_list = []
        for city in cities:
            cities_list.append(city.to_dict())
        return jsonify(cities_list)

    if request.method == 'POST':
        state = storage.get(State, state_id)
        if state is None:
            abort(404)

        city = request.get_json()
        if state is None:
            abort(400, description="Not a JSON")
        elif 'name' not in city:
            abort(400, description="Missing name")

        new_city = City(**city)
        new_city.state_id = state_id
        new_city.save()
        return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['GET'])
def cities(city_id):
    """Retrieves the list of a city objects
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    return make_response(jsonify(city.to_dict()), 200)


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """Deletes a City object
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """Updates a City object
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    city_data = request.get_json()
    if city_data is None:
        abort(400, description="Not a JSON")

    for key, value in city_data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)

    city.save()
    return make_response(jsonify(city.to_dict()), 200)
