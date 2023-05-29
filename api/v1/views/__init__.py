#!/usr/bin/python3
""" Initializing views """

from flask import Blueprint
#import api.v1.views.states

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
import api.v1.views.states
# __all__ = ['index']  # Ignore PEP8 warning for wildcard import
