from ngssm import app, auth, api
from flask import request, url_for, abort
from flask.ext.restful import Resource, reqparse, fields, marshal

from ngssm.entities.sample import Sample

sample_fields = {
		'plate': fields.String,
		'mid': fields.String,
		'mid_set': fields.String,
		'target': fields.String,
		'sff': fields.String,
		'location': fields.String,
		'primer_forward': fields.String,
		'primer_reverse': fields.String,
		'uri': fields.Url('sample')
}

class SampleAPI(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('plate', type = str, location = 'json')
		self.reqparse.add_argument('mid', type = str, location = 'json')
		self.reqparse.add_argument('mid_set', type = str, location = 'json')
		self.reqparse.add_argument('target', type = str, location = 'json')
		self.reqparse.add_argument('sff', type = str, location = 'json')
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
		session.delete(sample)
		session.commit()
		return { 'result': True }
	
class SampleListAPI(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('plate', type = str, default = "", location = 'json')
		self.reqparse.add_argument('mid', type = str, default = "", location = 'json')
		self.reqparse.add_argument('mid_set', type = str, default = "", location = 'json')
		self.reqparse.add_argument('target', type = str, default = "", location = 'json')
		self.reqparse.add_argument('sff', type = str, default = "", location = 'json')
		self.reqparse.add_argument('location', type = str, default = "", location = 'json')
		self.reqparse.add_argument('primer_forward', type = str, default = "", location = 'json')
		self.reqparse.add_argument('primer_reverse', type = str, default = "", location = 'json')
		super(SampleListAPI, self).__init__();

	@auth.login_required
	def post(self):

		args = self.reqparse.parse_args();

		if not 'plate' in args:
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
		for k, v in args.iteritems():
			if v != None and len(v) > 0:
				kwargs[k]=v

		if len(kwargs) > 0:
			print "Applying ", len(kwargs), " filters"
			query = query.filter_by(**kwargs)

		return { 'samples': marshal(query.all(), sample_fields), 'samples_count': query.count() }

api.add_resource(SampleListAPI, '/ngssm/api/v1.0/samples', endpoint = 'samples')
api.add_resource(SampleAPI, '/ngssm/api/v1.0/samples/<int:id>', endpoint = 'sample')

 


