#!/usr/bin/env bash
export LC_ALL=en_US.utf-8
export LANG=en_US.utf-8
export FLASK_DEBUG=True
export FLASK_APP=halal/__init__.py
export PROD_SETTINGS=/dev/null

if [ "$1" = "-r" ]
then
    echo "Creating DB"
    python createdb.py
fi

./node_modules/.bin/webpack --watch & # Run webpack (with watch) in background
flask run --host 127.0.0.1 --port 4141 --with-threads
