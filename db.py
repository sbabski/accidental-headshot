from pymongo import MongoClient
from bson import ObjectId
from pprint import pprint
#from extractor import *

client = MongoClient()
db = client.prepro
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


#user will specify name and favs to be placed in default project
def add_user(name, hashpass):
    #id = ObjectId()
    #project_comp = {'account': id, 'name': name, 'media': favs}
    #project = add_project(name+'_default', [project_comp])
    user = users.insert_one({'_id': id, 'name': name, 'password': hashpass, 'projects': []})
    return user.inserted_id

#create a project with name and preconstructed members
def add_project(name, members):
    project = projects.insert_one({'name': name, 'members': members})
    return project.inserted_id