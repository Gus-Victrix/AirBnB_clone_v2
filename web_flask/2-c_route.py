#!/usr/bin/python3

"""
Create a route for our website
"""

from flask import Flask
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index():
    """
    Display Hello HBNB to the root
    """
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """
    Display HBNB to the according route
    """
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def cIsFun(text):
    """
    Display c with the parameter
    """
    return 'C ' + text.replace('_', ' ')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
