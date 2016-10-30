from flask import Flask, render_template, request, redirect
import db

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
	userinputs = db.get_users()
	return render_template('index.html', userinputs=userinputs)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

