from peewee import *
from model.base import BaseModel

class Meals(BaseModel):
    title = CharField()
    img_url = CharField()
    description = CharField()
