#!/usr/bin/python3

"""
List all States through an end point
"""

from flask import Flask, render_template
from models import *
from models import storage
app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
    """
    teardown the database, to reset it.
    """
    storage.close()


@app.route('/hbnb_filters', strict_slashes=False)
def statesList():
    """
    list all states an amenities
    """
    states = sorted(list(storage.all("State").values()), key=lambda x: x.name)
    am = sorted(list(storage.all("Amenity").values()), key=lambda x: x.name)
    return render_template('10-hbnb_filters.html', states=states, amenities=am)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
