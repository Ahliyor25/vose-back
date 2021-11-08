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



    # layoutcategory = ForeignKeyField(LayoutCategory, on_delete='СASCADE')

class Residence(BaseModel):
    id = AutoField()
    img = CharField()
    title = CharField()
    description = CharField()
    img_2 = CharField(null = True)
    img_3 = CharField(null = True)
    location = CharField()
    typeEstate = CharField()
    term = CharField()
    imgYoutube = CharField(null = True)
    linkYoutube = CharField(max_length=255)
    titleTwo = CharField(max_length=200)
    desTwo = TextField()
    category = ForeignKeyField(CategoryObject, related_name='CategoryObjectId')
    
class Layout(BaseModel):
    id = AutoField()
    img = CharField()
    title = CharField(max_length=200)
    des = CharField(max_length=255)
    status = BooleanField(default=True)
    residence = ForeignKeyField(Residence, related_name='residences', on_delete='CASCADE')


class SendLayout(BaseModel):
    id = AutoField()
    layout = ForeignKeyField(Layout, related_name='sendlayouts')
    name = CharField(max_length = 50)
    phone = CharField(max_length= 100)
    button_text = CharField(max_length=100) 

class Services(BaseModel):
    id = AutoField()
    img = CharField()
    title = CharField()
    des = TextField()



class Spealization(BaseModel):
    id = AutoField()
    img = CharField()
    title = CharField()
    des = TextField()



class CategoryNS(BaseModel):
    id = AutoField()
    name = CharField()



class NS(BaseModel):
    id = AutoField()
    img = CharField()
    title = CharField(max_length=200)
    des = TextField()
    category = ForeignKeyField(CategoryNS, related_name='ns')

  

class Ids(BaseModel):
	id = AutoField()
	img = IntegerField()

if __name__ == '__main__':
    Users.create_table()
    MainSlider.create_table()
    TextSlider.create_table()
    CategoryObject.create_table()
    Residence.create_table()
    Layout.create_table()
    CategoryNS.create_table()
    Services.create_table()
    Spealization.create_table()
    NS.create_table()
    Ids.create_table()
    Ids(img=1).save()
    