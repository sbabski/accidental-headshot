from flask import Flask, render_template, request, redirect
import db2

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
	users = db2.get_users()
	return render_template('index.html', users=users)

@app.route('/<user>')
def user(user):
  if not user in db2.get_users_by_name():
    return redirect('/')
  else:
    person = db2.get_single_user(user)
    favs = []
    for fav in person['favs']:
      favs.append(db2.get_single_media_by_id(fav['media_id']))
    return render_template('user.html', person=person['name'], favs=favs)

if __name__ == "__main__":
    app.run(debug=True)

