#!/usr/bin/python3
"""Creates the status route
"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def status():
    """Displays the api status in JSON
    """
    return jsonify({"status": "OK"})
