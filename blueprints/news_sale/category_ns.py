from flask import blueprints,request, jsonify

from models import CategoryNS
from flask_jwt_extended.view_decorators import jwt_required
from peewee import *
bp  = blueprints.Blueprint('category_ns', __name__, url_prefix='/category_ns')

@bp.post('/')
@jwt_required()
def create_category_ns():
	_name = request.json.get('name')
	try:
		row = CategoryNS(
		name = _name
		)
		row.save()
		    
		response = jsonify("done")
		return response
	except Exception as e:
		return '{}'.format(e)

@bp.get('/')
def get_category_ns():
	try:
		categories = CategoryNS.select()
		js = []
		for i in categories:
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
		row = CategoryNS.get(CategoryNS.id == id)
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
		row = CategoryNS.get(CategoryNS.id == id)
	except DoesNotExist:
		return({"msg":"Не найден Text по такому id"})
	row.delete_instance()
	return jsonify("done")