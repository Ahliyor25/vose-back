
from os import path
from flask import Flask, jsonify, request, send_file
from flask import Blueprint
from flask_cors import cross_origin
from flask_jwt_extended.view_decorators import jwt_required
from peewee import Update
from models import *
from peewee import *
import os
from utils import helper_var, upload_image

bp = Blueprint('main_slider',__name__,url_prefix = '/main_slider')

path = helper_var.path
host  = helper_var.host

@bp.post('/')
@jwt_required()
def CreateSliderMain():
	
	target = os.path.join(path, 'images')

	if not os.path.isdir(target):
		os.mkdir(target)

	files =  request.files.getlist('img')
	if len(files) == 0:
		return jsonify(msg="FileNotFound")
	try:
		for file in files:
			name = Ids.get(Ids.id == 1).image
			filename = str(name) + file.filename[file.filename.index('.'):]
			destination = '/'.join([target, filename])
			file.save(destination)
			
			row = MainSlider(
				img = filename
			).save()
			
			a = Ids.get(Ids.id == 1)
			a.image = int(a.image) + 1
			a.save()
            
		
		response = jsonify("done")
		return response
	except Exception as e:
		return '{}'.format(e)

@bp.get('/')
def GetSlider():
	
	try:
		slider = MainSlider.select()
		
		js = []
	
		for i in slider:
			js.append({
				"id" : i.id,
				"img" : host + i.img,
			})
		return jsonify(js)
		
	except Exception as e:
		return '{}'.format(e)

@bp.put('/id')
@jwt_required()
def UpdateSlider():
	
	try:
		
		slider = MainSlider.get(MainSlider.id == id)

		img = request.files.getlist('img')
		
		if len(request.files(img)) == 0:
			slider.save()
			return jsonify('done')
		os.remove(helper_var.path + 'images/' + slider.icon)
		
		_img = upload_image(img)
	
		slider.img = _img
		slider.save()

		
		return jsonify("done")
		
	except Exception as e:
		return '{}'.format(e)


@bp.delete('/id')
@jwt_required()
def DeleteSlider():
	
	try:
		slider = MainSlider.get(MainSlider.id == id)

	except DoesNotExist:
		return({"msg":"Не найден слайдер по такому id"})	
	try:
		img_path = helper_var.path+'images/'+ slider.img
		if slider.img is not  None:
			os.remove(img_path)
		slider.delete_instance()
		return jsonify("done")
		
	except Exception as e:
		return '{}'.format(e)
