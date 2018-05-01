"""
Main API Routes for the React Application. Serves data to the frontend

Hassaan Ali Wattoo <hawattoo@umich.edu>
"""

import datetime
from flask import Blueprint, request, render_template, \
    flash, g, session, redirect, url_for, jsonify
import random
from halal import app, data
from pprint import pprint


# Set the route and accepted methods
@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Returns a JSON response containing all the halal courses served across UofM for today
    Sample Response

    { "data":
    [
        {   'dining_hall': 'Bursley Dining Hall',
            'date' : '2018-04-09',
            'meals':[
                {'name': 'Breakfast',
                 'start_time': '2018-04-09-08:00'
                 'end_time: '2018-04-09-12:00',
                 'courses':[
                    {'name': 'Signature',
                        'menuitems': [
                            {'name': 'Cornflake Chicken',
                             "allergens":
                                {"eggs": "eggs",
                                 "milk": "milk",
                                 "soy": "soy",
                                 "wheat_barley_rye": "wheat/barley/rye"
                                 },
                             "serving_size": "piece"
                             }
                        ]
                    }
                ]
            }
        }
    ]
    }

    :return:
    """
    return "Hello"
