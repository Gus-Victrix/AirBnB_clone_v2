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


@app.route('/hbnb', strict_slashes=False)
def statesList():
    """
    Render template for all hbnb
    """
    states = sorted(list(storage.all("State").values()), key=lambda x: x.name)
    amenities = sorted(list(storage.all("Amenity").values()), key=lambda x: x.name)
    places = sorted(list(storage.all("Place").values()), key=lambda x: x.name)
    print(places)
    return render_template('100-hbnb.html', states=states, amenities= amenities, places=places)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
