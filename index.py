from flask import Flask, render_template, request, redirect
import os
from pymongo import MongoClient

def connect():
	connection = MongoClient('ds053176.mlab.com', 53176)
	handle = connection['sarah']
	handle.authenticate('sarah', 'bei.pfi')
	return handle


app = Flask(__name__)
handle = connect()


@app.route('/', methods=['GET'])
def index():
	userinputs = [x for x in handle.mycollection.find()]
	return render_template('index.html', userinputs=userinputs)

@app.route('/write', methods=['POST'])
def write():
	userinput = request.form.get('userinput')
	oid = handle.mycollection.insert({'message':userinput})
	return redirect ('/')

@app.route('/deleteall', methods=['GET'])
def deleteall():
	handle.mycollection.remove()
	return redirect ('/')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
