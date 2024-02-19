#!/usr/bin/python3

"""
List all States through an end point
"""

from flask import Flask, render_template
from models import State
from models import storage
from markupsafe import escape
from models.state import State

app = Flask(__name__)


@app.teardown_appcontext
def teardown_db(exception):
    """
    teardown the database, to reset it.
    """
    storage.close()


@app.route('/states', strict_slashes=False)
def statesList():
    """
    list all states
    """
    states = storage.all(State)
    return render_template('9-states.html', states=states, choice=True)


@app.route('/states/<id>', strict_slashes=False)
def statesCityList(id):
    """
    list all states an cities
    """
    for state in storage.all(State).values():
        if state.id == id:
            return render_template('9-states.html', states=state, choice=False)
    return render_template('9-states.html', states=False, choice=False)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
