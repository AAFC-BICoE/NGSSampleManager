#!ngssmenv/bin/python

from entities.base import Base
from entities.sample import Sample
from entities.run import Run

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from flask import Flask, jsonify, make_response
from flask.ext.httpauth import HTTPBasicAuth
from flask.ext.restful import Api
 
auth = HTTPBasicAuth()
app = Flask(__name__, static_url_path = "")
api = Api(app)

import views.sample
import views.run

app.config.update(dict(
	DATABASE_URI="sqlite:///ngssm.db",
	DEBUG=True,
	USERNAME='miguel',
	PASSWORD='python',
# De-comment following line to make the app visible across the network.
#	HOST='0.0.0.0'
))
app.config.from_envvar('APP_SETTINGS', silent=True)

def connect_db():
	"""Connects to the specified database."""
	engine = create_engine(app.config['DATABASE_URI'], echo=True)
	Base.metadata.create_all(engine)
	app.session_maker = sessionmaker(bind=engine)


@auth.get_password
def get_password(username):
	if username == app.config['USERNAME']:
		return app.config['PASSWORD']
	return None
 
@auth.error_handler
def unauthorized():
	return make_response(jsonify( { 'error': 'Unauthorized access' } ), 403)
	# return 403 instead of 401 to prevent browsers from displaying the default auth dialog
	
@app.errorhandler(400)
def not_found(error):
	return make_response(jsonify( { 'error': 'Bad request' } ), 400)
 
@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify( { 'error': 'Not found' } ), 404)
 

@app.route('/')
def root():
	return app.send_static_file('index.html')


if __name__ == '__main__':
	connect_db()
	app.run()

