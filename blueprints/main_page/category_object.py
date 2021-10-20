from os import path
from flask import  json, jsonify, request, send_file
from flask import Blueprint
from flask_cors import cross_origin
from werkzeug.utils import validate_arguments
from models import *
from peewee import *
import os
from utils import helper_var

bp = Blueprint('category_object',__name__,url_prefix = '/category_object')

path = helper_var.path
host  = helper_var.host

@bp.post('/')
@cross_origin()
def CreateText():
    		
	_name = request.json.get('name')
	try:
		row = CategoryObject(
		name = _name
		)
		row.save()
		    
		response = jsonify("done")
		return response
	except Exception as e:
		return '{}'.format(e)

@bp.get('/')
@cross_origin()
def GetText():
	
	try:
		res = CategoryObject.select()
		js = []
		for i in res:
			js.append({
				"id" : i.id,
				"name": i.name,
			})
		return jsonify(js)
	except Exception as e:
		return '{}'.format(e)