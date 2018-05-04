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


@app.route('/halal/', methods=['GET'])
def halal():
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
    return jsonify(data.fetch_menus(datetime.datetime.now()))


@app.route('/halal/<year>/<month>/<day>/', methods=['GET'])
def halal_by_date(year, month, day):
    """
    Returns a JSON response containing all the halal courses served across UofM for the
    specified date
    Sample Response same as index

    :return:
    """
    date = datetime.datetime(int(year), int(month), int(day), 0, 0)
    return jsonify(data.fetch_menus(date))
