"""
Main API Routes for the React Application. Serves data to the frontend

Hassaan Ali Wattoo <hawattoo@umich.edu>
"""

import datetime
from flask import (
    Blueprint,
    request,
    render_template,
    flash,
    g,
    session,
    redirect,
    url_for,
    jsonify,
)
import random
from halal import app, data
from pprint import pprint


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")
