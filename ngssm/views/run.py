from ngssm import app, auth, api
from flask import request, url_for, abort
from flask.ext.restful import Resource, reqparse, fields, marshal

from ngssm.entities.run import Run

run_fields = {
		'type': fields.String,
		'mid_set': fields.String,
		'plate': fields.String,
		'uri': fields.Url('run')
}

run_uris = {
		'uri': fields.Url('run')
}

class RunAPI(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('type', type = str, location = 'json')
		self.reqparse.add_argument('mid_set', type = str, location = 'json')
		self.reqparse.add_argument('plate', type = str, location = 'json')
		super(RunAPI, self).__init__();

	@auth.login_required
	def get(self, id):
		session = app.session_maker()
		run = session.query(Run).filter_by(id=id).first();
		print "Run id: ", id, " Run: ", run
		if run == None:
			abort(404)
		return { 'run': marshal(run, run_fields) }

	@auth.login_required
	def put(self, id):
		session = app.session_maker()
		run = session.query(Run).filter_by(id=id).first()
	
		args = self.reqparse.parse_args();

		if run == None:
			abort(404)

		for k, v in args.iteritems():
			if v != None:
				setattr(run,k,v)

		session.commit()
		return { 'run': marshal(run, run_fields) }
		
	@auth.login_required
	def delete(self, id):
		session = app.session_maker()
		run = session.query(Run).filter_by(id=id).first()
		if run == None:
			abort(404)
		session.delete(run)
		session.commit()
		return { 'result': True }
	
class RunListAPI(Resource):
	def __init__(self):
		self.postreqparse = reqparse.RequestParser()
		self.postreqparse.add_argument('type', type = str, default = "", location = 'json')
		self.postreqparse.add_argument('mid_set', type = str, default = "", location = 'json')
		self.postreqparse.add_argument('plate', type = str, default = "", location = 'json')
		self.postreqparse.add_argument('sequencing_notes', type = str, default = "", location = 'json')

		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('type', type = str, default = "")
		self.reqparse.add_argument('mid_set', type = str, default = "")
		self.reqparse.add_argument('plate', type = str, default = "")
		self.reqparse.add_argument('sequencing_notes', type = str, default = "")
		super(RunListAPI, self).__init__();

	@auth.login_required
	def post(self):

		args = self.postreqparse.parse_args();

		run = Run()
		for k, v in args.iteritems():
			if v != None:
				setattr(run,k,v)

		session = app.session_maker()
		session.add(run)
		session.commit()

		return { 'run': marshal(run, run_fields) } , 201

	@auth.login_required
	def get(self):
		session = app.session_maker()
		query = session.query(Run)

		args = self.reqparse.parse_args();

		# build a dictionary and then unpack it into
		# the filter_by arguments using **
		kwargs = {}
		for k, v in args.iteritems():
			if v != None and len(v) > 0:
				kwargs[k]=v

		if len(kwargs) > 0:
			print "Applying ", len(kwargs), " filters"
			query = query.filter_by(**kwargs)

		return { 'runs': marshal(query.all(), run_uris), 'run_count': query.count() }

api.add_resource(RunListAPI, '/ngssm/api/v1.0/runs', endpoint = 'runs')
api.add_resource(RunAPI, '/ngssm/api/v1.0/runs/<int:id>', endpoint = 'run')
