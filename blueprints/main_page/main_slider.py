
from os import path
from flask import Flask, jsonify, request, send_file
from flask import Blueprint
from flask_cors import cross_origin
from models import *
from peewee import *
import os
from utils import helper_var

bp = Blueprint('main_slider',__name__,url_prefix = '/main_slider')

path = helper_var.path
host  = helper_var.host

@bp.post('/create')
@cross_origin()
def CreateSliderMain():
	
	target = os.path.join(path, 'images')

	if not os.path.isdir(target):
		os.mkdir(target)

	files =  request.files.getlist('file')
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

@bp.get('/get')
@cross_origin()
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