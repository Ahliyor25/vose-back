"""
Module Utils.py
A set of functions that are needed for the project
"""


from flask.json import jsonify
import os
from hashlib import sha256
from werkzeug.utils import find_modules, import_string
from models import Ids
from peewee import *


class helper_var:
    host = "http://192.168.0.115:9000/getimg/"
    path = "C:\\vose1\\vose-back/"





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

def register_blueprints_news_sale(app):
    """
    Searches all blueprints in folder blueprints/news_sale
    """
    for name in find_modules('blueprints.news_sale'):
        mod = import_string(name)
        if hasattr(mod, 'bp'):
            app.register_blueprint(mod.bp)

def register_blueprints_layout(app):
    """
    Searches all blueprints in folder blueprints/layout
    """
    for name in find_modules('blueprints.layout'):
        mod = import_string(name)
        if hasattr(mod, 'bp'):
            app.register_blueprint(mod.bp)

def register_blueprints_about(app):
    """
    Searches all blueprints in folder blueprints/about
    """
    for name in find_modules('blueprints.about'):
        mod = import_string(name)
        if hasattr(mod, 'bp'):
            app.register_blueprint(mod.bp)



def hash_string_sha256(to_hash):
    """
    Hashes string to sha256
    """
    return sha256(to_hash.encode()).hexdigest()


def upload_image(files):
    
    """
    Upload image files
    """

    target = os.path.join(helper_var.path, 'images')
    if not os.path.isdir(target):
        os.mkdir(target)
    if len(files) == 0:
    	return jsonify(msg="FileNotFound")

    for file in files:
        name = Ids.get(Ids.id == 1).img
        filename = str(name) + file.filename[file.filename.index('.'):]
        destination = '/'.join([target, filename])
        file.save(destination)
        
    a = Ids.get(Ids.id == 1)
    a.img = int(a.img) + 1
    a.save()
    
    return filename