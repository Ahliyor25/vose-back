from flask import blueprints,request, jsonify

from models import CategoryNS
from flask_jwt_extended.view_decorators import jwt_required

bp  = blueprints.Blueprint('category_ns', __name__, url_prefix='/category_ns')

@bp.post('/')
@jwt_required()
def create_category_ns():
	try:
		data = request.get_json('name')
		CategoryNS.create(
			data)
		return jsonify({'message':'Category created successfully'})
	except Exception as e:
		return '{}'.format(e), 301

@bp.get('/')
@jwt_required()
def get_category_ns():
	try:
		data = CategoryNS.get_all()
		return jsonify(data)
	except Exception as e:
		return '{}'.format(e), 301