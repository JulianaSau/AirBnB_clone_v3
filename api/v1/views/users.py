#!/usr/bin/python3
"""Creates views for User objects that handles all default RESTFul API action
"""

from api.v1.views.index import app_views
from flask import jsonify, abort, request, make_response

from models import storage
from models.user import User


@app_views.route('/users', methods=['GET', 'POST'])
def users():
    """Retrieves the list of all User objects
    """
    if request.method == 'GET':
        users = storage.all(User)
        users_list = []
        for user in users.values():
            users_list.append(user.to_dict())

        return jsonify(users_list)

    if request.method == 'POST':
        user = request.get_json()
        if user is None:
            abort(400, description="Not a JSON")
        elif 'email' not in user:
            abort(400, description="Missing email")
        elif 'password' not in user:
            abort(400, description="Missing password")

        new_user = User(**user)
        new_user.save()
        return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Retrieves a User object
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Deletes a User object
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Updates a User object
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    updated_user = request.get_json()
    if updated_user is None:
        abort(400, description="Not a JSON")

    # now to update the User object with all
    # key-value pairs of the dictionary. Ignore keys:
    # id, email, created_at and updated_at
    for key, value in updated_user.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)

    storage.save()

    return make_response(jsonify(user.to_dict()), 200)
