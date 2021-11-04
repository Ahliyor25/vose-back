from os import path
from flask import  json, jsonify, request, send_file
from flask import Blueprint
from flask_cors import cross_origin
from flask_jwt_extended.view_decorators import jwt_required
from werkzeug.utils import validate_arguments
from models import *
from peewee import *
import os
from utils import helper_var

bp = Blueprint('main_text',__name__,url_prefix = '/main_text')

path = helper_var.path
host  = helper_var.host

@bp.post('/')
@jwt_required()
def CreateText():
    		
	_company_des = request.json.get('company_des')
	_title = request.json.get('title')
	_des = request.json.get('des')
	_company = request.json.get('company')
	
	try:
		row = TextSlider(
		company_des = _company_des,
		title = _title,
		des = _des,
		company = _company)
		row.save()
		response = jsonify("done")
		return response
	except Exception as e:
		return '{}'.format(e)

@bp.get('/')
def GetText():
	
	try:
		res = TextSlider.select()
		js = []
		for i in res:
			js.append({
				"id" : i.id,
				"company_des": i.company_des,
				"title": i.title,
				"des" : i.des,
				"company" : i.company
			})
		return jsonify(js)
	except Exception as e:
		return '{}'.format(e)

@bp.put('/<id>')
@jwt_required()
def UpdateText(id):
	
	try:
		_company_des = request.json.get('company_des')
		_title = request.json.get('title')
		_des = request.json.get('des')
		_company = request.json.get('company')
		
		res = TextSlider.update(
		company_des = _company_des,
		title = _title,
		des = _des,
		company = _company).where(TextSlider.id == id)
		res.execute()
		return jsonify("done")
	except Exception as e:
		return '{}'.format(e)

@bp.delete('/<id>')
@jwt_required()
def DeleteText(id):
	
	try:
		res = TextSlider.delete().where(TextSlider.id == id)
		res.execute()
		return jsonify("done")
	except Exception as e:
		return '{}'.format(e)

