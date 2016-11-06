from flask import Flask, render_template, request, redirect
import db

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
	users = db.get_users()
	return render_template('index.html', users=users)

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
    app.run(debug=True)

