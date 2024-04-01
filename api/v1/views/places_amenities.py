#!/usr/bin/python3
"""Creates the place-amneity link routes
"""

from api.v1.views.index import app_views
from flask import jsonify, abort, request, make_response
from os import getenv
from models.amenity import Amenity
from models.place import Place
from models import storage


@app_views.route("/places/<place_id>/amenities", methods=['GET'])
def place_amenities(place_id):
    """Retrieves all the amenities of a place
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    amenities_lst = []
    if getenv("HBNB_TYPE_STORAGE") == "db":
        amenities_lst = [amenity.to_dict() for amenity in place.amenities]
    else:
        for id in place.amenity_ids:
            amenity = storage.get(Amenity, id)
            amenities_lst.append(amenity.to_dict())

    return jsonify(amenities_lst)


@app_views.route(
            "/places/<place_id>/amenities/<amenity_id>",
            methods=['DELETE', 'POST']
            )
def create_or_delete_amenity(place_id, amenity_id):
    """Creates or deletes an amenity by id
    """

    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)

    strg_type = getenv("HBNB_TYPE_STORAGE")
    json_dct = {}
    status_code = 200

    if request.method == 'DELETE':
        if amenity not in place.amenities:
            abort(404)

        if strg_type == 'db':
            place.amenities.remove(amenity)
        else:
            place.amenity_ids.remove(amenity_id)

    elif request.method == 'POST':
        json_dct = amenity.to_dict()
        if amenity not in place.amenities:
            if strg_type == 'db':
                place.amenities.append(amenity)
            else:
                place.amenity_ids.append(amenity_id)

            status_code = 201

    storage.save()

    return make_response(jsonify(json_dct), status_code)
