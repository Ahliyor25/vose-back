
from os import path

from flask import  jsonify, request, send_file
from flask import Blueprint
from flask_jwt_extended.view_decorators import jwt_required
from models import *
from peewee import *
import os
from utils import helper_var, upload_image

bp = Blueprint('ns',__name__,url_prefix = '/ns')

path = helper_var.path
host  = helper_var.host



@bp.post('/')
@jwt_required()
def create_residence():
	try:
		img = request.files.getlist('img')
		_img = upload_image(img)
		data = request.form.get
		ns = NS(
			img = _img,
			title = data('title'),
			des = data('des'),
			category = data('category'),
			)
		ns.save()
		return jsonify({'message':'success'})
	except Exception as e:
		return '{}'.format(e)

@bp.get('/')
def get_ns():
	try:
		ns = NS.select()
		js = []

		for n in ns:
			js.append({
				'id':n.id,
				'img':host + n.img,
				'title':n.title,
				'des':n.des,
				'category':n.category_id,
				})
		return jsonify({'data':js})
	except Exception as e:
		return '{}'.format(e)

@bp.put('/<id>')
@jwt_required()
def update_ns(id):
	try:
		ns = NS.get_by_id(id)
		data = request.form.get
		ns.title = data('title')
		ns.des = data('des')
		ns.category = data('category')

		if ns.img:
			img = request.files.getlist('img')
			if len(img) > 0:
				_img = upload_image(img)
				ns.img = _img
				ns.save()
				return jsonify({'message':'success'})
			else:
				return jsonify({'message':'error'})
		else:
			img = request.files.getlist('img')
			_img = upload_image(img)
			ns.img = _img
			ns.save()
			return jsonify({'message':'success'})
	except Exception as e:
		return '{}'.format(e)

@bp.delete('/<id>')
@jwt_required()
def delete_ns(id):
	try:
		ns = NS.get_by_id(id)
	except DoesNotExist:
		return({"msg":"Не найден проект по такому id"})
	try:

		img_path = helper_var.path+'images/'+ ns.img
		if ns.img is not  None:
			os.remove(img_path)
		ns.delete_instance()
		return jsonify({'message':'success'})
	except Exception as e:
		return '{}'.format(e)
