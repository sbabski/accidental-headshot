from flask import Flask, render_template, request, redirect, url_for, session
import bcrypt
import db

app = Flask(__name__)

@app.route('/')
def index():
  if 'username' in session:
    user = db.users.find_one({'name': session['username']})
    return render_template('home.html', user=user)
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
    f = request.form
    print(f)
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
