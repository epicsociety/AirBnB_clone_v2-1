#!/usr/bin/python3
""" Initializing views """

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *

__all__ = ['index']  # Ignore PEP8 warning for wildcard import
