
from os import path

from flask import  jsonify, request, send_file
from flask import Blueprint
from flask_jwt_extended.view_decorators import jwt_required
from models import *
from peewee import *
import os
from utils import helper_var, upload_image

bp = Blueprint('news',__name__,url_prefix = '/news')

path = helper_var.path
host  = helper_var.host



@bp.post('/')
@jwt_required()
def create_residence():
	try:
		img = request.files.getlist('img')
		_img = upload_image(img)
		data = request.form.get
		residence = Residence(
			img = _img,
			title = data('title'),
			description = data('description'),
			location = data('location'),
			typeEstate = data('typeEstate'),
			term = data('term'),
			linkYoutube = data('linkYoutube'),
			titleTwo = data('titleTwo'),
			desTwo = data('desTwo'),
			category = data('category'),
			)
		residence.save()
		return jsonify({'message':'success'})
	except Exception as e:
		return '{}'.format(e)

@bp.get('/')
def get_residence():
	try:
		residences = Residence.select()
		residences = [{
			'id':residence.id,
			'img':host + residence.img,
			'title':residence.title,
			'description':residence.description,
			'location':residence.location,
			'typestate':residence.typeEstate,
			'term':residence.term,
			'linkYoutube':residence.linkYoutube,
			'titleTwo':residence.titleTwo,
			'desTwo':residence.desTwo,
			'category':residence.category_id,
		} for residence in residences]
		return jsonify(residences)
	except Exception as e:
		return '{}'.format(e)

@bp.put('/<id>')
@jwt_required()
def update_residence(id):
	try:
		residence = Residence.get_by_id(id)
		data = request.form.get
		residence.title = data('title')
		residence.description = data('description')
		residence.location = data('location')
		residence.typeEstate = data('typeEstate')
		residence.term = data('term')
		residence.linkYoutube = data('linkYoutube')
		residence.titleTwo = data('titleTwo')
		residence.desTwo = data('desTwo')
		residence.category = data('category')

		if residence.img:
			img = request.files.getlist('img')
			if len(img) > 0:
				_img = upload_image(img)
				residence.img = _img
				residence.save()
				return jsonify({'message':'success'})
			else:
				return jsonify({'message':'error'})
		else:
			img = request.files.getlist('img')
			_img = upload_image(img)
			residence.img = _img
			residence.save()
			return jsonify({'message':'success'})
	except Exception as e:
		return '{}'.format(e)

@bp.delete('/<id>')
@jwt_required()
def delete_residence(id):
	try:
		residence = Residence.get_by_id(id)
	except DoesNotExist:
		return({"msg":"Не найден проект по такому id"})
	try:

		img_path = helper_var.path+'images/'+ residence.img
		if residence.img is not  None:
			os.remove(img_path)
		residence.delete_instance()
		return jsonify({'message':'success'})
	except Exception as e:
		return '{}'.format(e)
