# uofm-halal

[![Build Status](https://travis-ci.com/hassaanaliw/uofm-halal.svg?branch=master)](https://travis-ci.com/hassaanaliw/uofm-halal)

A React and Flask App that displays all marked Halal (Zabiha) courses being served at University of Michigan Dining Halls

# Setup Environments and Run

I've provided a small shell script to install the node dependencies

``` 
pip install -r requirements.txt
./install-all.sh
```

You can then run the flask app one of two ways

``` ./rundb.sh -r ``` rebuilds the database and runs the server

``` ./rundb.sh ``` only runs the server

# Project Structure

The project consists of two major aspects: the Flask Backend and the React Frontend

### Flask 

The flask app is contained in the halal directory. It contains several python files

1) database.py: Builds the database from the provided JSON files
2) data.py:     Packages the database info into a JSON format
3) api.py:      Provides the API routes that are used by the React frontend to retrieve data
4) views.py:    Renders the HTML files
5) models.py:   Defines the entire Database Schema. 

### React 

Currently the react app consists of one parent component that renders one further child component. 

The react app calls the routes defined in api.py to retrieve data and can be found in the halal/jsx/ folder.

Once the react files are compiled by webpack, the resultant bundle is placed in static/js_bundles

### Notes 

* This repository does not include the actual
JSON menu scraper or the JSON files so it will
not do much in its current state

* This currently displays the courses that have
been explicitly marked halal by the university. 
This doesn't mean that the vegetarian courses
served by the halls aren't halal but that there is no 
need to mark them as halal explicitly.



