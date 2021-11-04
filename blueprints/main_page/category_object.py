from os import path
from flask import  json, jsonify, request
from flask import Blueprint
from flask_jwt_extended.view_decorators import jwt_required
from models import *
from peewee import *
import os
from utils import helper_var

bp = Blueprint('category_object',__name__,url_prefix = '/category_object')

path = helper_var.path
host  = helper_var.host

@bp.post('/')
@jwt_required()
def Create():
    		
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

@bp.put('/<id>')
@jwt_required()
def UpdateText(id):
	try:
		_name = request.json.get('name')
		row = CategoryObject.get(CategoryObject.id == id)
	except DoesNotExist:
		return({"msg":"Не найден Text по такому id"})
	try:	
		row.name = _name
		row.save()
		return jsonify("done")
	except Exception as e:
		return '{}'.format(e)

@bp.delete('/<id>')
@jwt_required()
def DeleteText(id):
	try:
		row = CategoryObject.get(CategoryObject.id == id)
	except DoesNotExist:
		return({"msg":"Не найден Text по такому id"})
	row.delete_instance()
	return jsonify("done")
