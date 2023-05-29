#!/usr/bin/python3
""" Test .get() and .count() methods
"""
from models import storage
from models.state import State
from models.state import City
import json

print("All objects: {}".format(storage.count()))
print("State objects: {}".format(storage.count(State)))
print("City objects: {}".format(storage.count(City)))

first_state_id = list(storage.all(State).values())[0].id
print("First state: {}".format(storage.get(State, first_state_id)))

city_ids = list(storage.all(City).values())
for city_id in city_ids:
    print("Cities: {}".format(city_id.to_dict()))
