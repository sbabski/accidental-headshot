from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.datastructures import ImmutableMultiDict
from flask_sqlalchemy import SQLAlchemy
import bcrypt
import db

app = Flask(__name__)
app.config.from_pyfile('config.py')
db2 = SQLAlchemy(app)

# Create our database model
'''class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, email):
        self.email = email

    def __repr__(self):
        return '<E-mail %r>' % self.email'''

@app.route('/')
def index():
  if 'username' in session:
    user = db.users.find_one({'name': session['username']})
    return render_template('home.html', user=user)
  #reg = User('test')
  #db2.session.add(reg)
  #db2.session.commit()
  return render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
  if request.method == 'POST':
    name = request.form['username']
    exists = db.users.find_one({'name': name})
    if exists:
      if bcrypt.hashpw(request.form['password'].encode('utf-8'), exists['password']) == exists['password']:
        session['username'] = name
        return redirect(url_for('index'))

    return 'Invalid credentials'

  return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
  if request.method == 'POST':
    name = request.form['username']
    exists = db.users.find_one({'name': name})
    if exists is None:
      hashpass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
      db.add_user(name, hashpass)
      session['username'] = name
      return redirect(url_for('index'))

    return 'That username already exists!'

  return render_template('register.html')

@app.route('/create-taste-profile', methods=['POST', 'GET'])
def create():
  if request.method == 'POST':
    f = dict(request.form);
    result = ''
    comps = []
    if f['customtype'][0] == 'fromname':
      #check if length is right
      media_name = f['medianame']
      media_list = []
      for i  in range(0, len(media_name)):
        single = db.add_media(media_name[i], f['mediatype'][i], f['mediatype'][i])
        #error throwing for incomplete extraction
        single_list = []
        for s in single:
          #has to be revised: need object id of media already, should be done in db
          single_list.append(db.add_trope(s, media_name[i]))
        media_list.append(single_list)
      #member = db.add_member(f['username'], False, media_list)
      comp = {'name': f['username'], 'account': False, 'media': media_list}
      comps.append(member)
      #s = session['username']
    members = [session['username']]
    #add ref to this in all users projects
    #project = add_project(f['projectname'], members)
    project = {'name': f['projectname'], 'components': components, 'members': members}
    #add project to user and any users with account = True
    return str(project)

  users = db.users.find()
  projects = db.projects.find()
  return render_template('create.html', users=users)

@app.route('/logout')
def logout():
  session.pop('username')
  return(redirect(url_for('index')))


@app.route('/<user>')
def user(user):
  if not user in db.get_users_by_name():
    return redirect('/')
  else:
    person = db.get_single_user(user)
    return render_template('user.html', person=person['name'])

if __name__ == "__main__":
    app.secret_key = 'belarussianmafia'
    app.run(host='0.0.0.0', debug=True)

