from pymongo import MongoClient
from bson import ObjectId
from pprint import pprint
from extractor import *

client = MongoClient()
db = client.prepro
users = db.users
medias = db.media
tropes = db.tropes
projects = db.projects

#methods for flask
def get_users():
  return list(users.find())

def get_users_by_name():
  return list(users.distinct('name'))

def get_single_user(name):
  return users.find_one({'name': name})


#create a user on their first signin
def add_user(name, hashpass):
  #id = ObjectId()
  #project_comp = {'account': id, 'name': name, 'media': favs}
  #project = add_project(name+'_default', [project_comp])
  user = users.insert_one({'name': name, 'password': hashpass, 'projects': []})
  return user.inserted_id

#create a project with name and preconstructed members
def add_project(name, comps, members):
  #project = projects.insert_one({'name': name, 'members': members, 'components': comps})
  #return project.inserted_id
  project = {'name': name, 'components': comps, 'members': members}
  return project

#create subcategory of project
def add_component(name, account, media):
  return {'name': name, 'account': account, 'media': media}

#create a media element and construct requisite tropes
def add_media(title, type_of, weight):
  #check if already added
  tropes = parse_page(title, type_of)
  return tropes
  #return {'title': title, 'type': type_of}
  #media = medias.insert_one({'name': name, 'type': type_of, 'tropes': tropes})
  #return media.inserted_id

#create a trope element to be run through extractor
def add_trope(url, media):
  #check if already added
  #trope = tropes.insert_one({'title': title})
  #return trope.inserted_id
  result = {'url': url, 'media': [media]}
  return result
