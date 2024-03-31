#!/usr/bin/python3
"""Creates views for State objects that handles all default RESTFul API action
"""

from api.v1.views.index import app_views
from flask import jsonify, abort, request, make_response

from models import storage
from models.state import State


@app_views.route('/states', methods=['GET', 'POST'])
def states():
    """Retrieves the list of all State objects
    """
    if request.method == 'GET':
        states = storage.all(State)
        states_list = []
        for state in states.values():
            states_list.append(state.to_dict())

        return jsonify(states_list)

    if request.method == 'POST':
        state = request.get_json()
        if state is None:
            return "Not a JSON", 400
        elif 'name' not in state:
            return "Missing name", 400

        new_state = State(**state)
        new_state.save()
        return jsonify(new_state.to_dict(), 201)


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """Retrieves a State object
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """Deletes a State object
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """Updates a State object
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    updated_state = request.get_json()
    if updated_state is None:
        return "Not a JSON", 400
    elif updated_state.get('name') is None:
        return "Missing name", 400

    # now to update the State object with all 
    # key-value pairs of the dictionary. Ignore keys: 
    # id, created_at and updated_at
    for key, value in updated_state.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)

    storage.save()

    return make_response(jsonify(state.to_dict()), 200)

        