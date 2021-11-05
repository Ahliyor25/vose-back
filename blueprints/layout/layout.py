from os import path

from flask import  jsonify, request, send_file
from flask import Blueprint
from flask_jwt_extended.view_decorators import jwt_required
from models import *
from peewee import *
import os
from utils import helper_var, upload_image

bp = Blueprint('layout',__name__,url_prefix = '/layout')

path = helper_var.path
host  = helper_var.host



@bp.post('/')
@jwt_required()
def create_layout():
	try:
		img = request.files.getlist('img')
		_img = upload_image(img)
		data = request.form.get
		ns = Layout(
			img = _img,
			title = data('title'),
			des = data('des'),
            status = data('status'),
			residence = data('residence_id'),
            
			)
		ns.save()
		return jsonify({'message':'success'})
	except Exception as e:
		return '{}'.format(e)

@bp.get('/')
def get_layout():
    try:
        p = request.args.get('page',1)
        layouts = Layout.select().order_by(Layout.id).paginate(int(p),6) 
        count = Layout.select().count()
        js = {"count" : 0, 'layout' : []}
        if count%6==0:
            js['count'] = count//6
        elif count>6:
            js['count'] = count//6+1
        else:
            js['count'] = 1
        for l in layouts:
            js['layout'].append({
                'id' : l.id,
                'img' : host + l.img,
                'title' : l.title,
                'des' : l.des,
                'status' : l.status,
                'residence' : l.residence_id,})
        return jsonify(js)
    except Exception as e:
        return '{}'.format(e)
    



@bp.put('/<id>')
@jwt_required()
def update_layout(id):
    try:
        layout = Layout.get_by_id(id)
        data = request.form.get
        layout.title = data('title')
        layout.des = data('des')
        layout.status = data('status')
        layout.residence = data('residence_id')

        if layout.img:
            img = request.files.getlist('img')
            if len(img) > 0:
                _img = upload_image(img)
                layout.img = _img
                layout.save()
                return jsonify({'message':'success'})
            else:
                layout.save()
                return jsonify({'message':'success'})
		    
        else: 
            img = request.files.getlist('img')
            _img = upload_image(img)
            layout.img = _img
            layout.save()
            return jsonify({'message':'success'})
    except Exception as e:
        return '{}'.format(e)

@bp.delete('/<id>')
@jwt_required()
def delete_layout(id):
    try:
        layout = Layout.get_by_id(id)
    except DoesNotExist:
	    return({"msg":"Не найден проект по такому id"})
    try:
        img_path = helper_var.path+'images/'+ layout.img
        if layout.img is not  None:
            os.remove(img_path)
        layout.delete_instance()
        return jsonify({'message':'success'})
    except Exception as e:
        return '{}'.format(e)
    
    