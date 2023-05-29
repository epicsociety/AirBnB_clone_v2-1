#!/usr/bin/python3
""" Airbnb flask app """

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import environ

host = environ.get('HBNB_API_HOST', default='0.0.0.0')
port = environ.get('HBNB_API_PORT', default='5000')

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """ close storage """
    storage.close()


@app.errorhandler(404)
def error_404(error):
    """ returns the not found """
    response = jsonify({"error": "Not found"})
    response.status_code = 404
    return response


if __name__ == "__main__":
    app.run(debug=True, host=host, port=port, threaded=True)
