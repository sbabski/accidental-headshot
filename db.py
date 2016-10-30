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

#test simple add and complex add for media
#do those for tropes


#test: last version had 36 shoutout across gm and aw, this has 35 (3 are akira)

#fixes:
# make sure only first in ul

#fix triple akira issue - poss fixed
#add cb

def add_user(name, favs=[]):
  if(len(favs) != 25):
    print('List needs to have 25 items')
    return 0

  def build():
    fav_results = []
    for item in favs:
      media_id = add_media(item[1], item[0])
      fav_results.append({'media_id': media_id, 'weight': item[2]})
    return {'name': name, 'favs': fav_results}

  return add_document(users, {'name': name}, build)

def add_project(name, people=[]):
  if(len(people) < 2):
    print ('List needs to have at least two users')
    return 0

  toAdd = []
  for user in people:
    userCursor = list(users.find({'name': user}))
    if len(userCursor) == 0:
      print(user + ' does not exist')
      return 0
    else:
      toAdd.append(userCursor[0]['_id'])

  def build():
    t = list(getAggregateTropes(toAdd))
    return {'name': name, 'users': toAdd, 'tropes': t}

  return add_document(projects, {'users': toAdd}, build)

def add_media(title, type):
  def build():
    tropes = parse_page(title, type)
    trope_list = []
    for item in tropes:
      trope_list.append(add_trope_simple(item))
    return {'title': title, 'tropes': trope_list, 'type': type}

  return add_document(media, {'title': title}, build)

def add_media_simple(title, type):
  def build():
    return {'title':title, 'type': type}

def add_trope_simple(title):
  def build():
    return {'title': title}

  return add_document(tropes, {'title': title}, build)

def add_document(collection, query, builder):
  ex = collection.find(query)
  if ex.count() != 0:
    if ex.count() != 1:
      print('ERROR')
      return 0
    else:
      #if complex, need to see if it's previously been only simply added
      return ex[0]['_id']
  result = collection.insert_one(builder())
  return result.inserted_id


def getAggregateTropes(u):
  favs = users.aggregate([
    {'$match': {'_id': {'$in': u}}},
    {'$unwind': '$favs'},
    {'$group': {
      '_id': '$favs.media_id'
    }}
  ])
  return media.aggregate([

    {'$match': {'$or': list(favs)}},
    {'$unwind': '$tropes'},
    {'$group': {
      '_id': '$tropes',
      'total': {'$sum': 1},
      'media': {'$push': '$title'}
    }},
    {'$sort': {'total': -1}}
  ])

#users.drop()
#media.drop()
#tropes.drop()
#projects.drop()

#add_project('awgm', ['gm', 'aw'])
#add_project('mp', ['mood', 'plot'])

#sm = sitemapper('http://tvtropes.org/pmwiki/index_report.php')
#pprint(list(tropes.find()))
#print(trope_string)

'''def get_title(item):
  return item['title']
def filter_title(item):
  return 'main' in item

titles = list(map(get_title, list(tropes.find())))
titles = list(filter(filter_title, titles))
trope_string = '\n'.join(titles)
print(len(titles))
correct_titles = list(filter(filter_title, titles))
print(len(correct_titles))
with open('test_file.txt', 'w') as text_file:
  text_file.write(trope_string)'''

def getComboTopTropes(name, top):
  lt = list(projects.find({'name': name}))[0]['tropes']
  cap = lt[top-1]['total']
  def iterFind(ind, inc):
    return iterFind(ind+inc, inc) if lt[ind]['total'] == cap else ind
  result = iterFind(iterFind(top, 10) - 10, 1)
  return lt[:result]

def getComboMediaFromTrope(name, t):
  full_t = 'http://tvtropes.org/pmwiki/pmwiki.php/main/' + t
  return projects.aggregate([
    {'$match': {'name': name}},
    {'$unwind': '$tropes'},
    {'$match': {'tropes._id': list(tropes.find({'title': full_t}))[0]['_id']}}
  ])

def getComboRiseAndFall(first, second):
  return projects.aggregate([
    {'$match': {'name': {'$in': [first, second]}}},
    {'$unwind': '$tropes'},
    {'$group': {
      '_id': '$tropes._id',
      'totals': {'$push': '$tropes.total'}
    }},
    {'$project': {
      '_id': 1,
      'totals': 1,
      'name_size': {'$size': '$totals'}
    }},
    {'$match': {'name_size': {'$eq': 2}}},
    {'$project': {
      '_id': 1,
      'totals': 1,
      'diff': {'$subtract': [
        {'$arrayElemAt': ['$totals', 1]},
        {'$arrayElemAt': ['$totals', 0]}
      ]}
    }}
  ])

#pprint(list(projects.find()))
#pprint(list(getComboRiseAndFall('awgm', 'mp')))
#pprint(list(tropes.find({'_id': ObjectId('57ec37c628e54820bcd2cad4')})))
#pprint(list(getComboMediaFromTrope('awgm', 'bittersweetending')))

#pprint(parse_page_trope('CrooksAreBetterArmed'))
#pprint(parse_page_trope('holodeckmalfunction'))

'''add_user('cb', [
  ['series', 'breaking bad', 1],
  ['series', 'twin peaks', 1],
  ['western animation', 'bobs burgers', 1],
  ['series', 'parks and recreation', 1],
  ['film', 'twelve monkeys', 1],
  ['film', 'pulp fiction', 1],
  ['film', 'my own private idaho', 1],
  ['film', 'fight club', 1],
  ['film', 'metropolis', 1],
  ['disney', 'the lion king', 1],
  ['film', 'interstellar', 1],
  ['film', 'blade runner', 1],
  ['film', 'three hundred', 1],
  ['film', 'jurassic park', 1],
  ['film', 'saving private ryan', 1],
  ['film', 'two thousand one a space odyssey', 1],
  ['film', 'the grand budapest hotel', 1],
  ['film', 'psycho', 1],
  ['film', 'the dark knight', 1],
  ['film', 'raiders of the lost ark', 1],
  ['film', 'the rocky horror picture show', 1],
  ['film', 'stand by me', 1],
  ['film', 'the shining', 1],
  ['film', 'beetlejuice', 1],
  ['film', 'clueless', 1]
])

add_user('sb', [
  ['film', 'the evil dead'],
  ['film', 'blade runner'],
  ['film', 'jurassic park'],
  ['film', 'amelie'],
  ['anime', 'spirited away'],
  ['film', 'alien'],
  ['film', 'magnolia'],
  ['film', 'the big lebowski'],
  ['film', 'north by northwest', 1],
  ['film', 'rushmore'],
  ['film', 'ghostbusters'],
  ['film', 'the thing'],
  ['film', 'the grand budapest hotel'],
  ['disney', 'robin hood'],
  ['film', 'time bandits'],
  ['film', 'brazil'],
  ['film', 'beetlejuice'],
  ['film', 'lost in translation'],
  ['film', 'two thousand one a space odyssey'],
  ['film', 'pans labyrinth'],
  ['film', 'district nine'],
  ['film', 'the maltese falcon'],
  ['film', 'sunset boulevard'],
  ['film', 'clue'],
  ['film', 'clueless'],
  ['film', 'raiders of the lost ark'],
  ['film', 'oldboy'],
  ['film', 'city of lost children'],
  ['film', 'children of men'],
  ['film', 'spy kids'],
  ['film', 'we are the best'],
  ['film', 'labyrinth'],
  ['film', 'the master'],
  ['film', 'it follows'],
  ['anime', 'akira'],
  ['film', 'trainspotting'],
  ['film', 'battle royale'],
  ['film', 'submarine'],
  ['disney', 'the lion king'],
  ['film', 'twelve monkeys'],
  ['film', 'arsenic and old lace'],
  ['film', 'shaun of the dead'],
  ['film', 'frank'],
  ['film', 'double indemnity'],
  ['series', 'the x files'],
  ['series', 'twin peaks', 1],
  ['western animation', 'over the garden wall'],
  ['series', 'dead like me'],
  ['series', 'pushing daisies'],
  ['series', 'the thick of it'],
  ['series', 'hannibal'],
  ['series', 'parks and recreation'],
  ['western animation', 'bobs burgers'],
  ['series', 'star trek the next generation'],
  ['anime', 'cowboy bebop'],
  ['western animation', 'rick and morty'],
  ['series', 'the kids in the hall'],
  ['series', 'the mighty boosh'],
  ['series', 'a bit of fry and laurie'],
  ['series', 'garth marenghis darkplace'],
  ['series', 'peep show'],
  ['western animation', 'archer'],
  ['series', 'its always sunny in philadelphia'],
  ['series', 'black books'],
  ['series', 'mad men'],
  ['series', 'house of cards'],
  ['series', 'look around you']
])'''

add_user('plot', [
    ["western animation", "ratchet and clank", 1],
    ["series", "kikaider", 1],
    ["film", "the matrix", 1],
    ["film", "daft punks electroma", 1],
    ["literature", "a wind named amnesia", 1],
    ["film", "tetsuo the iron man", 1],
    ["film", "eden log", 1],
    ["film", "deadly friend", 1],
    ["film", "la jetee", 1],
    ["series", "extant", 1],
    ["film", "quintet", 1],
    ["literature", "the lathe of heaven", 1],
    ["film", "existenz", 1],
    ["film", "repo men", 1],
    ["anime", "sailor moon crystal", 1],
    ["film", "chronicle", 1],
    ["anime", "cowboy bebop", 1],
    ["film", "the city of lost children", 1],
    ["anime", "rahXephon", 1],
    ["film", "cyborg", 1],
    ["anime", "the place promised in our early days", 1],
    ["anime", "toward the terra", 1],
    ["manga", "venus wars", 1],
    ["anime", "elfen lied", 1],
    ["film", "the maze runner", 1]
])

add_user('moodplot', [
    ["anime", "ghost in the shell", 1],
    ["anime", "metropolis", 1],
    ["anime", "neon genesis evangelion", 1],
    ["anime", "ergo proxy", 1],
    ["series", "buck rogers in the twenty fifth century", 1],
    ["anime", "memories", 1],
    ["film", "the time machine 2002", 1],
    ["anime", "akira", 1],
    ["film", "screamers", 1],
    ["manga", "strait jacket", 1],
    ["film", "oblivion 2013", 1],
    ["film", "virtuosity", 1],
    ["anime", "wolfs rain", 1],
    ["film", "millennium", 1],
    ["anime", "the big o", 1],
    ["film", "blade runner", 1],
    ["anime", "attack on titan", 1],
    ["film", "robo cop 1987", 1],
    ["film", "twelve monkeys", 1],
    ["film", "i am legend", 1],
    ["film", "johnny mnemonic", 1],
    ["film", "event horizon", 1],
    ["film", "two thousand one a space odyssey", 1],
    ["anime", "towa no quon", 1],
    ["film", "surrogates", 1]
])

add_user('mood', [
    ["film", "the red circle", 1],
    ["film", "heat", 1],
    ["anime", "kill la kill", 1],
    ["anime", "patlabor", 1],
    ["film", "mad max beyond thunderdome", 1],
    ["film", "batman", 1],
    ["anime", "night raid 1931", 1],
    ["film", "kill bill", 1],
    ["franchise", "zatoichi", 1],
    ["film", "the quick and the dead", 1],
    ["film", "snake eyes", 1],
    ["film", "spies", 1],
    ["film", "a chinese ghost story", 1],
    ["film", "cube", 1],
    ["manga", "x 1999", 1],
    ["light novel", "no 6", 1],
    ["literature", "ivanhoe", 1],
    ["film", "the beach", 1],
    ["anime", "earth maiden arjuna", 1],
    ["manga", "lone wolf and cub", 1],
    ["film", "the lord of the rings", 1],
    ["series", "treasure island 2012", 1],
    ["film", "the giver", 1],
    ["series", "gotham", 1],
    ["film", "a fistful of dollars", 1]
])

add_user('aw', [
    ["western animation", "the last unicorn", 1],
    ["film", "the dark crystal", 1],
    ["film", "scream1996", 1],
    ["film", "alien", 1],
    ["film", "requiem for a dream", 1],
    ["film", "a scanner darkly", 1],
    ["film", "blow", 1],
    ["film", "goodfellas", 1],
    ["film", "sixteen candles", 1],
    ["anime", "kikis delivery service", 1],
    ["film", "clueless", 1],
    ["film", "rebecca", 1],
    ["film", "thirteen", 1],
    ["anime", "castle in the sky", 1],
    ["film", "valley girl", 1],
    ["anime", "howls moving castle", 1],
    ["anime", "ghost in the shell", 1],
    ["anime", "blood the last vampire", 1],
    ["series", "skins", 1],
    ["anime", "flcl", 1],
    ["anime", "samurai champloo", 1],
    ["anime", "ergo proxy", 1],
    ["western animation", "the boondocks", 1],
    ["western animation", "south park", 1],
    ["anime", "digimon adventure", 1]
])

add_user('gm', [
    ["film", "the professional", 1],
    ["film", "the big lebowski", 1],
    ["film", "pulp fiction", 1],
    ["film", "fight club", 1],
    ["film", "two thousand one a space odyssey", 1],
    ["film", "kill bill", 1],
    ["film", "magnolia", 1],
    ["film", "yojimbo", 1],
    ["film", "requiem for a dream", 1],
    ["film", "the thin red line", 1],
    ["film", "dr strangelove", 1],
    ["film", "his girl friday", 1],
    ["film", "rushmore", 1],
    ["film", "mad max 2 the road warrior", 1],
    ["film", "amelie", 1],
    ["film", "high noon", 1],
    ["anime", "ghost in the shell", 1],
    ["anime", "akira", 1],
    ["anime", "cowboy bebop", 1],
    ["anime", "samurai champloo", 1],
    ["anime", "dragon ball z", 1],
    ["series", "lost", 1],
    ["series", "the x files", 1],
    ["western animation", "family guy", 1],
    ["series", "star trek the next generation", 1]
])
