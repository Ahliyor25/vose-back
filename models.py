import datetime
from peewee import *

db = SqliteDatabase('db1.db')

class BaseModel(Model):
    class Meta:
        database = db

class Users(BaseModel):
    id = AutoField()
    username = CharField()
    password = CharField()

class MainSlider(BaseModel):
    id = AutoField()
    img = CharField()

class Ids(BaseModel):
	id = AutoField()
	image = IntegerField()

if __name__ == '__main__':
    Users.create_table()
    MainSlider.create_table()
    Ids.create_table()
    #Ids(image=1).save()
    