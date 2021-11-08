
from os import link, path
import re
from flask import  jsonify, request, send_file
from flask import Blueprint
from flask_jwt_extended.view_decorators import jwt_required
from models import *
from peewee import *
import os
from utils import helper_var, upload_image

bp = Blueprint('residence',__name__,url_prefix = '/residence')

path = helper_var.path
host  = helper_var.host



@bp.post('/')
@jwt_required()
def create_residence():
	
	img = request.files.getlist('img')
	if request.files['img'].filename == '':
		return jsonify({'message':'No file [img] selected'}),400
	else:
		_img = upload_image(img)

	img2 = request.files.getlist('img2')
	img3 = request.files.getlist('img3')
	imgYoutube = request.files.getlist('imgYoutube')

	data = request.form.get

	
	if request.files['img2'].filename == '':
		_img2 = None
	else:
		_img2 = upload_image(img2)

	if  request.files['img3'].filename == '':
		_img3 = None
		
	else:
		_img3 = upload_image(img3)

	if request.files['imgYoutube'].filename == '':
		_imgYoutube = None
		
	else:
		_imgYoutube = upload_image(imgYoutube)
		
			
	try:
		residence = Residence(
			img = _img,
			title = data('title'),
			description = data('description'),
			location = data('location'),
			img_2 = _img2,
			img_3 = _img3,
			typeEstate = data('typeEstate'),
			term = data('term'),
			imgYoutube = _imgYoutube,
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
		p = request.args.get('page',1)
		residences = Residence.select().order_by(Residence.id).paginate(int(p),6) 
		count = Residence.select().count()
		js = {"count" : 0, 'residence' : []}
		if count%6==0:
		    js['count'] = count//6
		elif count>6:
			js['count'] = count//6+1
		else:
			js['count'] = 1

		for residence in residences:

		 js['residence'].append({
			 'id':residence.id,
			'img':host + residence.img,
			'title':residence.title,
			'description':residence.description,
			"img2" : residence.img_2 if residence.img_2 is None else  host + residence.img_2,
			"img3" : residence.img_3 if residence.img_3 is None else  host + residence.img_3,
			'location':residence.location,
			'typestate':residence.typeEstate,
			'term':residence.term,
			"imgYoutube" : residence.imgYoutube if residence.imgYoutube is None else  host + residence.imgYoutube,
			'linkYoutube':residence.linkYoutube,
			'titleTwo':residence.titleTwo,
			'desTwo':residence.desTwo,
			'category_id':residence.category_id,
		 })
			
		return jsonify(js)
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
