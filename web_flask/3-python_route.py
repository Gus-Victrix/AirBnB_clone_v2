#!/usr/bin/python3

"""
Create a route for our website
"""

from flask import Flask, escape
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    """Return value"""
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hello_HBNB():
    """Return value"""
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def hello_C(text):
    """Return value"""
    return 'C {}'.format(text.replace('_', ' '))


@app.route('/python', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def hello_Python(text="is cool"):
    """Return value"""
    return 'Python {}'.format(text.replace('_', ' '))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
