#!/usr/bin/python3.8

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


@app.route('/states_list', strict_slashes=False)
def statesList():
    """
    list all states
    """
    states = sorted(list(storage.all("State").values()), key=lambda x: x.name)
    return render_template('7-states_list.html', states=states)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
