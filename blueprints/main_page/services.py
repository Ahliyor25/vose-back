import os
from re import S
from flask import  Blueprint,jsonify,request
from flask_jwt_extended.view_decorators import jwt_required

from models import Services
from utils import helper_var, upload_image
from peewee import *

bp = Blueprint('services',__name__, url_prefix='/services')


path = helper_var.path
host  = helper_var.host

@bp.post('/')
@jwt_required()
def create_service():
    try:
        data  = request.form.get
        img = request.files.getlist('img')
        _img = upload_image(img)

        Services(
            img = _img,
            title = data('title'),
            des = data('des'),
        ).save()
        return jsonify({'message':'Service created'})
    except Exception as e:
        return '{}'.format(e)

@bp.get('/')
def get_service():
    try:
        p = request.args.get('page',1)
        services = Services.select().order_by(Services.id).paginate(int(p),6) 
        count = Services.select().count()
        js = {"count" : 0, 'services' : []}
        if count%6==0:
            js['count'] = count//6
        elif count>6:
            js['count'] = count//6+1
        else:
            js['count'] = 1
        for s in services:
            js['services'].append({
                'id' : s.id,
                'img' : host + s.img,
                'title' : s.title,
                'des' : s.des})
        return jsonify(js)
    except Exception as e:
        return '{}'.format(e)

@bp.put('/<id>')
@jwt_required()
def update_service(id):
    try:
        services = Services.get_by_id(id)
        data = request.form.get
        services.title = data('title')
        services.des = data('des')

        if services.img:
            img = request.files.getlist('img')
            if len(img) > 0:
                _img = upload_image(img)
                services.img = _img
                services.save()
                return jsonify({'message':'success'})
            else:
                services.save()
                return jsonify({'message':'success'})
		    
        else: 
            img = request.files.getlist('img')
            _img = upload_image(img)
            services.img = _img
            services.save()
            return jsonify({'message':'success'})
    except Exception as e:
        return '{}'.format(e)

@bp.delete('/<id>')
@jwt_required()
def delete_layout(id):
    try:
        services = Services.get_by_id(id)
    except DoesNotExist:
	    return({"msg":"Не найден проект по такому id"})
    try:
        img_path = helper_var.path+'images/'+ services.img
        if services.img is not  None:
            os.remove(img_path)
        services.delete_instance()
        return jsonify({'message':'success'})
    except Exception as e:
        return '{}'.format(e)
    