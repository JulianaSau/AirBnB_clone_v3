#!/usr/bin/python3
"""Creates views for Amenity objects that handles all default RESTFul API action
"""

from api.v1.views.index import app_views
from flask import jsonify, abort, request, make_response

from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET', 'POST'])
def amenities():
    """Retrieves the list of all Amenity objects
    """
    if request.method == 'GET':
        amenities = storage.all(Amenity)
        amenities_list = []
        for amenity in amenities.values():
            amenities_list.append(amenity.to_dict())

        return jsonify(amenities_list)

    if request.method == 'POST':
        amenity = request.get_json()
        if amenity is None:
            return "Not a JSON", 400
        elif 'name' not in amenity:
            return "Missing name", 400

        new_amenity = Amenity(**amenity)
        new_amenity.save()
        return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    """Retrieves a Amenity object
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """Deletes a Amenity object
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """Updates a Amenity object
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    updated_amenity = request.get_json()
    if updated_amenity is None:
        return "Not a JSON", 400
    elif updated_amenity.get('name') is None:
        return "Missing name", 400

    # now to update the Amenity object with all
    # key-value pairs of the dictionary. Ignore keys:
    # id, created_at and updated_at
    for key, value in updated_amenity.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)

    storage.save()

    return make_response(jsonify(amenity.to_dict()), 200)
