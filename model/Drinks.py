from peewee import *
from model.base import BaseModel

class Drinks(BaseModel):
    title = CharField()
    img_url = CharField()
    description = CharField()
