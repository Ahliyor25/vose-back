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
    position = IntegerField()
    img = CharField()
     


if __name__ == '__main__':
    Users.create_table()