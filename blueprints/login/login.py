from utils import hash_string_sha256, upload_image, helper_var
from flask import Flask, jsonify, request, send_file
from flask_jwt_extended import (
	JWTManager, jwt_required, create_access_token,
	get_jwt_identity, decode_token
)
from flask import Blueprint
from flask_cors import cross_origin
from models import *
from peewee import *

bp = Blueprint('login',__name__,url_prefix = '/login')

host  = helper_var.host

@bp.post('/')
@cross_origin()
def LogIn():
	try:
		_username = request.json.get('username')
		_password = request.json.get('password')
		
		query = Users.select().where((Users.username == _username))
		if not query.exists():
			return jsonify({"msg": "DoesNotExists"})
		for i in query:
			if i.password == hash_string_sha256(_password):
				access_token = create_access_token(identity=i.username)
				response = jsonify({"id": i.id,
				"username": i.username,
				"password" : i.password,
				"name" : i.name,
				"email": i.email,
				"role" : i.role,
				"status" : i.status,
				"img": host + i.img,

				"access_token" : access_token })
				return response
			else: return ({"msg":"Не правильный пароль"})
	except Exception as e:
		return '{}'.format(e)


@bp.post('/signup')

@cross_origin()
def SignUp():
	try:
	#id username password name email phone
		_username = request.form.get('username')
		_password = request.form.get('password')
		_name =  request.form.get('name')
		_email = request.form.get('email')
		_role = request.form.get('role')
		_status = request.form.get('status')
		avatar = request.files.getlist('img')
	
		_avatar = upload_image(avatar)

		access_token = create_access_token(identity=_username)
		us = Users( username = _username,
		 password = hash_string_sha256(_password),
		 name = _name,
		 email = _email,
		 role = _role,
		 status = _status,
		 img = _avatar
		 )
		us.save()
		return jsonify(access_token=access_token), 200
	except Exception as e:
		return '{}'.format(e)



			


@bp.put('/update_user/<id>')
@cross_origin()
def UpdateUser(id):
	
	try:
		usr = Users.get(Users.id == id)
	except DoesNotExist:
		return({"msg":"Не найден User по такому id"})
	
	try:
		usr.username  = request.form.get('username')
		usr.password =  request.form.get('password')
		usr.name = request.form.get('name')
		usr.email = request.form.get('email')
		usr.role = request.form.get('role')
		usr.status = request.form.get('status')

		usr.save()
		response = jsonify('done')
		return response
	except Exception as e:
			return '{}'.format(e)
			
@bp.get('/get_users')
@cross_origin()
def GetUser():
	try:
		p = request.args.get('page',1)
		prj = Users.select().order_by(Users.id).paginate(int(p),6)
		count = Users.select().count()
		js = {"count" : 0, 'users' : []}
		if count%6==0:
			js['count'] = count//6
		elif count > 6:
			js['count'] = count //6 + 1
		else:
			js['count'] = 1
		for i in prj:
			js['users'].append({
				"id" : i.id,
			
				"username" : i.username,
				"name" : i.name,
				"email": i.email,
				"role" : i.role,
				"status" : i.status,
				"img": host + i.img,
				
			})
		return jsonify(js)
	except Exception as e:
			return '{}'.format(e)
			
@bp.delete('/del_users/<id>')

@cross_origin()
def UsersDelete(id):
	try:
		a = Users.get(Users.id == id)
	except DoesNotExist:
		return({"msg":"Не найден Users  по такому id"})	
	try:
		a.delete_instance()
		return jsonify({"msg" : "Done"})
	except Exception as e:
		return '{}'.format(e)