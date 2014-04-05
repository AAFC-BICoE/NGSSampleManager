import os
import base64
import ngssm
import unittest
import tempfile
from selenium import webdriver

from ngssm.entities.sample import Sample

#class SeleniumWebTests(unittest.TestCase):
#	def testSanity(self):
#		"""Dummy test to ensure things are working"""
#		self.assertEqual(1,1)
#
#	def setUp(self):
#		ngssm.app.config['DATABASE_URI'] = "sqlite:///test.db"
#		ngssm.app.config['TESTING'] = True
#		self.app = ngssm.app.test_client()
#		ngssm.connect_db()
#		self.browser = webdriver.Firefox()
#
#	def tearDown(self):
#		os.unlink("test.db")
#		self.browser.quit()
#
#	def testConnect(self):
#		self.browser.get('http://localhost:5000/index.html')
#		self.assertIn("Metagenomics", self.browser.title)

class CodeTests(unittest.TestCase):
	def testSanity(self):
		"""Dummy test to ensure things are working"""
		self.assertEqual(1,1)

	def testPassword(self):
		"""Test hardcoded password is returned for hardcoded user"""
		self.assertEqual(ngssm.get_password('miguel'), 'python')

class ApplicationContextTests(unittest.TestCase):
	def get_headers(self, json):
		h = {
			'Authorization': 'Basic ' + 
					base64.b64encode(
						ngssm.app.config['USERNAME'] + ":" + 
						ngssm.app.config['PASSWORD']
					),
		}
		if json:
			h['Content-Type'] = 'application/json';
		return h

	def setUp(self):
		ngssm.app.config['DATABASE_URI'] = "sqlite:///test.db"
		ngssm.app.config['TESTING'] = True
		self.app = ngssm.app.test_client()
		ngssm.connect_db()

	def tearDown(self):
		os.unlink("test.db")

	def testSanity(self):
		"""Dummy test to ensure things are working"""
		self.assertEqual(1,1)

	def test_require_password(self):
		"""Test access to sample list without a password."""
		rv = self.app.get('/ngssm/api/v1.0/samples')
		assert 'Unauthorized access' in rv.data

	def test_empty_db(self):
		"""Verify that the sample count of the empty list is 0."""
		h = self.get_headers(False)
		rv = self.app.get('/ngssm/api/v1.0/samples',headers=h)
		assert '"samples_count": 0' in rv.data

	def test_add_sample(self):
		"""Verify addition of a sample.  Should have id 1 and sample count should be 1."""
		h = self.get_headers(False)
		hc = self.get_headers(True)
		rv = self.app.get('/ngssm/api/v1.0/samples', headers=h)
		print rv.data
		assert '"samples_count": 0' in rv.data
		rv = self.app.post('/ngssm/api/v1.0/samples', data='{"plate":"5.1"}', headers=hc)
		print rv.data
		assert 'samples/1' in rv.data
		rv = self.app.get('/ngssm/api/v1.0/samples', headers=h)
		print rv.data
		assert '"samples_count": 1' in rv.data

	def test_update_sample(self):
		"""Verify update of a sample."""
		h = self.get_headers(False)
		hc = self.get_headers(True)
		rv = self.app.get('/ngssm/api/v1.0/samples', headers=h)
		assert '"samples_count": 0' in rv.data
		rv = self.app.post('/ngssm/api/v1.0/samples', data='{"plate":"5.1"}', headers=hc)
		assert 'samples/1' in rv.data
		assert '"sff": ""' in rv.data
		rv = self.app.put('/ngssm/api/v1.0/samples/1', data='{"sff":"ASDG"}', headers=hc)
		assert '"sff": "ASDG"' in rv.data

	def test_update_sample_fail_type(self):
		"""Test assignment of boolean values to Sample fields.  PUT handler requires unicode, thus should fail."""
		h = self.get_headers(False)
		hc = self.get_headers(True)
		rv = self.app.get('/ngssm/api/v1.0/samples', headers=h)
		assert '"samples_count": 0' in rv.data
		rv = self.app.post('/ngssm/api/v1.0/samples', data='{"plate":"5.1"}', headers=hc)
		assert 'samples/1' in rv.data
		rv = self.app.put('/ngssm/api/v1.0/samples/1', data='{"sff":True}', headers=hc)
		print rv.data
		assert 'Bad Request' in rv.data
		rv = self.app.put('/ngssm/api/v1.0/samples/1', data='{"mid":True}', headers=hc)
		print rv.data
		assert 'Bad Request' in rv.data
		rv = self.app.put('/ngssm/api/v1.0/samples/1', data='{"mid_set":True}', headers=hc)
		print rv.data
		assert 'Bad Request' in rv.data
		rv = self.app.put('/ngssm/api/v1.0/samples/1', data='{"plate":True}', headers=hc)
		print rv.data
		assert 'Bad Request' in rv.data
		rv = self.app.put('/ngssm/api/v1.0/samples/1', data='{"target":True}', headers=hc)
		print rv.data
		assert 'Bad Request' in rv.data

	def test_delete_sample(self):
		"""Test deleting a sample"""
		h = self.get_headers(False)
		hc = self.get_headers(True)
		rv = self.app.get('/ngssm/api/v1.0/samples', headers=h)
		assert '"samples_count": 0' in rv.data
		rv = self.app.post('/ngssm/api/v1.0/samples', data='{"plate":"5.1"}', headers=hc)
		assert 'samples/1' in rv.data
		rv = self.app.delete('/ngssm/api/v1.0/samples/1', headers=h)
		print rv.data
		assert '"result": true' in rv.data

	def test_retrieve_sample_empty_list(self):
		"""Test retrieving a sample from an empty list"""
		h = self.get_headers(False)
		rv = self.app.get('/ngssm/api/v1.0/samples/1', headers=h)
		print rv.data
		assert '"status": 404' in rv.data

	def test_filter_sample_list(self):
		"""Test filtering a sample list"""
		h = self.get_headers(False)
		hc = self.get_headers(True)
		rv = self.app.get('/ngssm/api/v1.0/samples', headers=h)
		print rv.data
		assert '"samples_count": 0' in rv.data
		rv = self.app.post('/ngssm/api/v1.0/samples', data='{"plate":"5.1"}', headers=hc)
		assert 'samples/1' in rv.data
		rv = self.app.post('/ngssm/api/v1.0/samples', data='{"plate":"5.2"}', headers=hc)
		assert 'samples/2' in rv.data
		rv = self.app.get('/ngssm/api/v1.0/samples', headers=h)
		assert '"samples_count": 2' in rv.data
		print "Get: /ngssm/api/v1.0/samples?plate=5.1"
		rv = self.app.get('/ngssm/api/v1.0/samples?plate=5.1', headers=h)
		assert '"samples_count": 1' in rv.data



#	def test_make_public_sample(self):
#		"""Test ensures conversion of id to URI and removal of id"""
#		sample = Sample(id=1, plate="45.2")
#		self.assertFalse(hasattr(sample, 'uri'))
#		self.assertTrue(hasattr(sample, 'id'))
#		new_sample = ngssm.make_public_sample(sample)
#		self.assertIsNotNone(new_sample)
#		self.assertTrue(hasattr(new_sample), 'uri')
#		self.assertFalse(hasattr(new_sample), 'id')
