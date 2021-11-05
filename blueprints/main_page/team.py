import os
from flask import  Blueprint,jsonify,request
from flask_jwt_extended.view_decorators import jwt_required

from models import Team
from utils import helper_var, upload_image
from peewee import *

bp = Blueprint('team',__name__, url_prefix='/team')


path = helper_var.path
host  = helper_var.host

@bp.post('/')
@jwt_required()
def create_service():
    try:
        data  = request.form.get
        img = request.files.getlist('img')
        _img = upload_image(img)

        Team(
            img = _img,
            name = data('name'),
            position = data('position'),
            des = data('des'),
        ).save()
        return jsonify({'message':' Team created'})
    except Exception as e:
        return '{}'.format(e)

@bp.get('/')
def get_service():
    try:
        p = request.args.get('page',1)
        team = Team.select().order_by(Team.id).paginate(int(p),6) 
        count = Team.select().count()
        js = {"count" : 0, 'team' : []}
        if count%6==0:
            js['count'] = count//6
        elif count>6:
            js['count'] = count//6+1
        else:
            js['count'] = 1
        for t in team:
            js['team'].append({
                'id' : t.id,
                'img' : host + t.img,
                'name' : t.name,
                'position' : t.position,
                'des' : t.des})
        return jsonify(js)
    except Exception as e:
        return '{}'.format(e)

@bp.put('/<id>')
@jwt_required()
def update_team(id):
    try:
        team = Team.get_by_id(id)
    except DoesNotExist:
	    return({"msg":"Team not exist"})
    try:
        team.name  = request.form.get('name')
        img =   request.files.getlist('img')
        team.position = request.form.get('position')
        team.des  = request.form.get('des')
	    
        if len(img) == 0:
            team.save()
            return jsonify('done')
        os.remove(helper_var.path + 'images/' + team.img)	
		
        _img = upload_image(img)
	
        team.img = _img
        team.save()
	
        response = jsonify('done')
        return response
    except Exception as e:
        return '{}'.format(e)

@bp.delete('/<id>')
@jwt_required()
def delete_team(id):
    try:
        team = Team.get_by_id(id)
    except DoesNotExist:
	    return({"msg":"Не найден проект по такому id"})
    try:
        img_path = helper_var.path+'images/'+ team.img
        if team.img is not  None:
            os.remove(img_path)
        team.delete_instance()
        return jsonify({'message':'success'})
    except Exception as e:
        return '{}'.format(e)
    