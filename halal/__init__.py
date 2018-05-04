# Import flask and template operators
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

db = SQLAlchemy(app)

import halal.views
import halal.models
import halal.database


# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return 'Error, 404', 404
