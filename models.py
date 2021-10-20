import datetime
from re import A
from typing import Text
from peewee import *

db = SqliteDatabase('db1.db')

class BaseModel(Model):
    class Meta:
        database = db

class Users(BaseModel):
    id = AutoField()
    username = CharField()
    password = CharField()
    name = CharField()
    email = CharField()
    role = CharField()
    status = BooleanField()
    img = CharField()

class MainSlider(BaseModel):
    id = AutoField()
    img = CharField()

class TextSlider(BaseModel):
    id = AutoField()
    company_des = CharField()
    title = CharField()
    des = TextField()
    company = CharField()

class CategoryObject(BaseModel):
    id = AutoField()
    name = CharField()

class  Object(BaseModel):
    id = AutoField()
    img = CharField()
    title = CharField()
    description = CharField()
    img_2 = CharField()
    

    # layoutcategory = ForeignKeyField(LayoutCategory, on_delete='СASCADE')


    

class Ids(BaseModel):
	id = AutoField()
	image = IntegerField()

if __name__ == '__main__':
    Users.create_table()
    MainSlider.create_table()
    TextSlider.create_table()
    CategoryObject.create_table()
    Ids.create_table()
    #Ids(image=1).save()
    