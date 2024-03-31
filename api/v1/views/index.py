#!/usr/bin/python3
"""Creates the status route
"""

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route("/status")
def status():
    """Displays the api status in JSON
    """
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def stats():
    """Displays the objects count in JSON
    """
    objs_count = {
            "amenities": 0, "cities": 0, "places": 0, "reviews": 0,
            "states": 0, "users": 0
            }

    objs_count["amenities"] = storage.count(Amenity)
    objs_count["cities"] = storage.count(City)
    objs_count["places"] = storage.count(Place)
    objs_count["reviews"] = storage.count(Review)
    objs_count["states"] = storage.count(State)
    objs_count["users"] = storage.count(User)

    return jsonify(objs_count)
