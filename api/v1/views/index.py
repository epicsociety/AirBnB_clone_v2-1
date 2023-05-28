#!/usr/bin/python3
""" index file """


from api.v1.views import app_views
from flask import jsonify


app_views.route('/status', methods=['GET'])
def index_status():
    """ returns status as JSON"""
    return jsonify({"status": "OK"})
