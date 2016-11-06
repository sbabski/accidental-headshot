from flask import Flask, render_template, request, redirect, url_for, session
from flask.ext.login import LoginManager
import db

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@app.route('/', methods=['GET'])
def index():
  if 'username' in session:
    return 'You are logged in as' + session['username']
  users = db.get_users()
  return render_template('index.html', users=users)

@app.route('/login')
def login():
  return ''

@app.route('/<user>')
def user(user):
  if not user in db.get_users_by_name():
    return redirect('/')
  else:
    person = db.get_single_user(user)
    favs = []
    for fav in person['favs']:
      favs.append(db.get_single_media_by_id(fav['media_id']))
    return render_template('user.html', person=person['name'], favs=favs)

if __name__ == "__main__":
    app.secret_key = 'belarussianmafia'
    app.run(host='0.0.0.0', debug=True)

