from ngssm import app, auth, api
from flask import request, url_for, abort
from flask.ext.restful import Resource, reqparse, fields, marshal

from ngssm.entities.sample import Sample

sample_fields = {
		'run_id': fields.Integer,
		'mid': fields.String,
		'target': fields.String,
		'sff': fields.String,
		'location': fields.String,
		'sample': fields.String,
		'primer_forward': fields.String,
		'primer_reverse': fields.String,
		'uri': fields.Url('sample')
}

sample_uris = {
		'uri': fields.Url('sample')
}

class SampleAPI(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('run_id', type = int, location = 'json')
		self.reqparse.add_argument('mid', type = str, location = 'json')
		self.reqparse.add_argument('target', type = str, location = 'json')
		self.reqparse.add_argument('sff', type = str, location = 'json')
		self.reqparse.add_argument('location', type = str, location = 'json')
		self.reqparse.add_argument('sample', type = str, location = 'json')
		self.reqparse.add_argument('primer_forward', type = str, location = 'json')
		self.reqparse.add_argument('primer_reverse', type = str, location = 'json')
		super(SampleAPI, self).__init__();

	@auth.login_required
	def get(self, id):
		session = app.session_maker()
		sample = session.query(Sample).filter_by(id=id).first();
		print "Sample id: ", id, " Sample: ", sample
		if sample == None:
			abort(404)
		return { 'sample': marshal(sample, sample_fields) }

	@auth.login_required
	def put(self, id):
		session = app.session_maker()
		sample  = session.query(Sample).filter_by(id=id).first()
	
		args = self.reqparse.parse_args();

		if sample == None:
			abort(404)

		for k, v in args.iteritems():
			if v != None:
				setattr(sample,k,v)

		session.commit()
		return { 'sample': marshal(sample, sample_fields) }
		
	@auth.login_required
	def delete(self, id):
		print "Received delete request for: ", id
		session = app.session_maker()
		sample  = session.query(Sample).filter_by(id=id).first()
		if sample == None:
			abort(404)
		session.delete(sample)
		session.commit()
		return { 'result': True }
	
class SampleListAPI(Resource):
	def __init__(self):
		self.postreqparse = reqparse.RequestParser()
		self.postreqparse.add_argument('run_id', type = int, required = True, help="No run selected", location = 'json')
		self.postreqparse.add_argument('mid', type = str, default = "", location = 'json')
		self.postreqparse.add_argument('target', type = str, default = "", location = 'json')
		self.postreqparse.add_argument('sff', type = str, default = "", location = 'json')
		self.postreqparse.add_argument('location', type = str, default = "", location = 'json')
		self.postreqparse.add_argument('sample', type = str, default = "", location = 'json')
		self.postreqparse.add_argument('primer_forward', type = str, default = "", location = 'json')
		self.postreqparse.add_argument('primer_reverse', type = str, default = "", location = 'json')

		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('run_id', type = int, default = "")
		self.reqparse.add_argument('mid', type = str, default = "")
		self.reqparse.add_argument('target', type = str, default = "")
		self.reqparse.add_argument('sff', type = str, default = "")
		self.reqparse.add_argument('location', type = str, default = "")
		self.reqparse.add_argument('sample', type = str, default = "")
		self.reqparse.add_argument('primer_forward', type = str, default = "")
		self.reqparse.add_argument('primer_reverse', type = str, default = "")

		self.reqparse.add_argument('offset', type = int, default = 0)
		self.reqparse.add_argument('limit', type = int, default = 10)

		super(SampleListAPI, self).__init__();

	@auth.login_required
	def post(self):

		args = self.postreqparse.parse_args();

		if not 'run_id' in args:
			abort(400)
		
		sample = Sample()
		for k, v in args.iteritems():
			if v != None:
				setattr(sample,k,v)

		session = app.session_maker()
		session.add(sample)
		session.commit()

		return { 'sample': marshal(sample, sample_fields) } , 201

	@auth.login_required
	def get(self):
		session = app.session_maker()
		query = session.query(Sample)

		args = self.reqparse.parse_args();

		# build a dictionary and then unpack it into
		# the filter_by arguments using **
		kwargs = {}
		limit = args.get('limit')
		offset = args.get('offset')

		for k, v in args.iteritems():
			if v != None and k!= 'limit' and k!= 'offset' and ((type(v) == str and len(v) > 0) or (type(v) == int and v > 0)):
					kwargs[k]=v

		if len(kwargs) > 0:
			print "Applying ", len(kwargs), " filters"
			query = query.filter_by(**kwargs)

		return { 'samples': marshal(query.limit(limit).offset(offset).all(), sample_uris), 'sample_count': query.count(), 'next_page': '/ngssm/api/v1.0/samples?limit=' + str(limit) + '&offset=' + str(offset + limit) }

api.add_resource(SampleListAPI, '/ngssm/api/v1.0/samples', endpoint = 'samples')
api.add_resource(SampleAPI, '/ngssm/api/v1.0/samples/<int:id>', endpoint = 'sample')
