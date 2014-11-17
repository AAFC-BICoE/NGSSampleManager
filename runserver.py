#! ngssmenv/bin/python

from ngssm import app, connect_db, loadconfigs
from flask import Flask, jsonify, make_response
from flask.ext.httpauth import HTTPBasicAuth
from flask.ext.restful import Api

connect_db()
if 'HOST' in app.config:
  HOST=app.config['HOST']
else:
  HOST='127.0.0.1'

app.run(debug=True, host=HOST)

