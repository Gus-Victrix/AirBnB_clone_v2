#!/usr/bin/python3

"""
Create a route for our website
"""

from flask import Flask, escape
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


@app.route('/python', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python(text='is cool'):
    """
    Display python with the parameter, that got a default value
    """
    return 'python ' + text.replace('_', ' ')


@app.route('/number/<int:n>', strict_slashes=False)
def hello_number(n):
    """Return value"""
    return '{} is a number'.format(n)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
