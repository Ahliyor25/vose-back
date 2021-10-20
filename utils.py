"""
Module Utils.py
A set of functions that are needed for the project
"""


import json
import string
import random
from hashlib import sha256
from werkzeug.utils import find_modules, import_string


class helper_var:
    host = "192.168.0.134:9000/getimg/"
    path = 'C:\\vose_back'





# * Blueprints


def register_blueprints_login(app):
    """
    Searches all blueprints in folder blueprints/login
    """
    for name in find_modules('blueprints.login'):
        mod = import_string(name)
        if hasattr(mod, 'bp'):
            app.register_blueprint(mod.bp)

def register_blueprints_main_page(app):
    """
    Searches all blueprints in folder blueprints/main_page
    """
    for name in find_modules('blueprints.main_page'):
        mod = import_string(name)
        if hasattr(mod, 'bp'):
            app.register_blueprint(mod.bp)


# * Images


def get_id_of_image():
    """
    Get id of image in data.json
    """
    with open('data.json') as _file:
        data = json.load(_file)

    return data['avatar']


def update_id_name():
    """
    Update id of image in data.json
    """
    with open('data.json') as _file:
        data = json.load(_file)

    data['avatar'] += 1

    with open('data.json', 'w') as _file:
        json.dump(data, _file)



def hash_string_sha256(to_hash):
    """
    Hashes string to sha256
    """
    return sha256(to_hash.encode()).hexdigest()
