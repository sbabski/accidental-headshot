from pymongo import MongoClient
from bson import ObjectId
from pprint import pprint
from extractor import *

client = MongoClient()
db = client.preproduction
users = db.users
media = db.media
tropes = db.tropes
projects = db.projects

#methods for flask

def get_users():
  return list(users.find())

def get_users_by_name():
  return list(users.distinct('name'))

def get_single_user(name):
  return users.find_one({'name': name})

def get_single_media_by_id(id):
  return media.find_one({'_id': id})