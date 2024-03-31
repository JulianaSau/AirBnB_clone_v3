#!/usr/bin/python3
"""Module that defines the root route
"""

from flask import Flask, make_response, jsonify
from os import getenv
from flask_cors import CORS

from models import storage
from api.v1.views import app_views


app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})
app.url_map.strict_slashes = False
app.register_blueprint(app_views, url_prefix='/api/v1')


@app.errorhandler(404)
def not_found(error):
    """Handles  not found resources
    """
    return make_response(jsonify({"error": "Not found"}), 404)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': error.description}), 400)


@app.teardown_appcontext
def teardown(exc):
    """closes and reloads the storage session
    """
    storage.close()


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST") if getenv("HBNB_API_HOST") else "0.0.0.0"
    port = getenv("HBNB_API_PORT") if getenv("HBNB_API_PORT") else "5000"
    app.run(host=host, port=port,  threaded=True)
