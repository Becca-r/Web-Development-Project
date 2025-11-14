from peewee import *

db = SqliteDatabase('recipes.db')

class BaseModel:
    class Meta:
        database = db