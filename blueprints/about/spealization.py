import os
from flask import  Blueprint,jsonify,request
from flask_jwt_extended.view_decorators import jwt_required

from models import Spealization
from utils import helper_var, upload_image
from peewee import *

bp = Blueprint('spealization',__name__, url_prefix='/spealization')


path = helper_var.path
host  = helper_var.host

@bp.post('/')
@jwt_required()
def create_spealization():
    try:
        data  = request.form.get
        img = request.files.getlist('img')
        _img = upload_image(img)

        Spealization(
            img = _img,
            title = data('title'),
            des = data('des'),
        ).save()
        return jsonify({'message':' spealization created'})
    except Exception as e:
        return '{}'.format(e)

@bp.get('/')
def get_spealization():
    try:
        p = request.args.get('page',1)
        spealization = Spealization.select().order_by(Spealization.id).paginate(int(p),6) 
        count = Spealization.select().count()
        js = {"count" : 0, 'spealization' : []}
        if count%6==0:
            js['count'] = count//6
        elif count>6:
            js['count'] = count//6+1
        else:
            js['count'] = 1
        for s in spealization:
            js['spealization'].append({
                'id' : s.id,
                'img' : host + s.img,
                'title' : s.title,
                'des' : s.des})
        return jsonify(js)
    except Exception as e:
        return '{}'.format(e)

@bp.put('/<id>')
@jwt_required()
def update_spealization(id):
    try:
        spealization = Spealization.get_by_id(id)
    except DoesNotExist:
	    return({"msg":"Spealization not exist"})
    try:
        spealization.title  = request.form.get('title')
        img  =   request.files.getlist('img')
        spealization.des  = request.form.get('des')
	    
        if len(img) == 0:
            spealization.save()
            return jsonify('done')
        os.remove(helper_var.path + 'images/' + spealization.img)	
		
        _img = upload_image(img)
	
        spealization.img = _img
        spealization.save()
	
        response = jsonify('done')
        return response
    except Exception as e:
        return '{}'.format(e)

@bp.delete('/<id>')
@jwt_required()
def delete_spealization(id):
    try:
        spealization = Spealization.get_by_id(id)
    except DoesNotExist:
	    return({"msg":"Не найден проект по такому id"})
    try:
        img_path = helper_var.path+'images/'+ spealization.img
        if spealization.img is not  None:
            os.remove(img_path)
        spealization.delete_instance()
        return jsonify({'message':'success'})
    except Exception as e:
        return '{}'.format(e)