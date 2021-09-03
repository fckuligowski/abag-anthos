"""
The bags Blueprint handles the bag scan history.
"""
from flask import Blueprint
bags_blueprint = Blueprint('bags', __name__, template_folder='templates')

from . import routes
