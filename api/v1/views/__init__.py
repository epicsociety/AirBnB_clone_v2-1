#!/usr/bin/python3
""" Initializing views """

from flask import Blueprint
#import api.v1.views.states

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
import api.v1.views.states
import api.v1.views.cities
import api.v1.views.amenities
import api.v1.views.users
import api.v1.views.places
import api.v1.views.places_reviews
# __all__ = ['index']  # Ignore PEP8 warning for wildcard import
