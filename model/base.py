from peewee import *

db = SqliteDatabase('recipes.db')

class BaseModel(Model):
    class Meta:
        database = db