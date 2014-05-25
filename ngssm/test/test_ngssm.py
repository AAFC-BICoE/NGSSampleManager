import os
import base64
import ngssm
import unittest
import tempfile
from selenium import webdriver

from ngssm.entities.sample import Sample
from ngssm.entities.run import Run 

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

	def test_sample_require_password(self):
		"""Test access to sample list without a password."""
		rv = self.app.get('/ngssm/api/v1.0/samples')
		assert 'Unauthorized access' in rv.data

	def test_sample_list_empty_db(self):
		"""Verify that the sample count of the empty list is 0."""
		h = self.get_headers(False)
		rv = self.app.get('/ngssm/api/v1.0/samples',headers=h)
		assert '"sample_count": 0' in rv.data

	def test_sample_add(self):
		"""Verify addition of a sample.  Should have id 1 and sample count should be 1."""
		h = self.get_headers(False)
		hc = self.get_headers(True)

		# add required run
		rv = self.app.get('/ngssm/api/v1.0/runs', headers=h)
		print rv.data
		assert '"run_count": 0' in rv.data
		rv = self.app.post('/ngssm/api/v1.0/runs', data='{"plate":"5.1"}', headers=hc)
		print rv.data
		assert 'runs/1' in rv.data
	
		# add sample
		rv = self.app.get('/ngssm/api/v1.0/samples', headers=h)
		print rv.data
		assert '"sample_count": 0' in rv.data
		rv = self.app.post('/ngssm/api/v1.0/samples', data='{"run_id":"1"}', headers=hc)
		print rv.data
		assert 'samples/1' in rv.data

		# retrieve samples
		rv = self.app.get('/ngssm/api/v1.0/samples', headers=h)
		print rv.data
		assert '"sample_count": 1' in rv.data

	def test_sample_update(self):
		"""Verify update of a sample."""
		h = self.get_headers(False)
		hc = self.get_headers(True)

		# add required run
		rv = self.app.get('/ngssm/api/v1.0/runs', headers=h)
		print rv.data
		assert '"run_count": 0' in rv.data
		rv = self.app.post('/ngssm/api/v1.0/runs', data='{"plate":"5.1"}', headers=hc)
		print rv.data
		assert 'runs/1' in rv.data
	
		# add sample
		rv = self.app.get('/ngssm/api/v1.0/samples', headers=h)
		assert '"sample_count": 0' in rv.data
		rv = self.app.post('/ngssm/api/v1.0/samples', data='{"run_id":"1"}', headers=hc)
		assert 'samples/1' in rv.data
		assert '"sff": ""' in rv.data

		# update sample
		rv = self.app.put('/ngssm/api/v1.0/samples/1', data='{"sff":"ASDG"}', headers=hc)
		assert '"sff": "ASDG"' in rv.data

	def test_sample_update_fail_type(self):
		"""Test assignment of boolean values to Sample fields.  PUT handler requires unicode, thus should fail."""
		h = self.get_headers(False)
		hc = self.get_headers(True)

		# add required run
		rv = self.app.get('/ngssm/api/v1.0/runs', headers=h)
		print rv.data
		assert '"run_count": 0' in rv.data
		rv = self.app.post('/ngssm/api/v1.0/runs', data='{"plate":"5.1"}', headers=hc)
		print rv.data
		assert 'runs/1' in rv.data
	
		# add sample
		rv = self.app.get('/ngssm/api/v1.0/samples', headers=h)
		assert '"sample_count": 0' in rv.data
		rv = self.app.post('/ngssm/api/v1.0/samples', data='{"run_id":"1"}', headers=hc)
		assert 'samples/1' in rv.data

		# fail updates
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

	def test_sample_delete(self):
		"""Test deleting a sample"""
		h = self.get_headers(False)
		hc = self.get_headers(True)

		# add required run
		rv = self.app.get('/ngssm/api/v1.0/runs', headers=h)
		print rv.data
		assert '"run_count": 0' in rv.data
		rv = self.app.post('/ngssm/api/v1.0/runs', data='{"plate":"5.1"}', headers=hc)
		print rv.data
		assert 'runs/1' in rv.data
	
		# add sample
		rv = self.app.get('/ngssm/api/v1.0/samples', headers=h)
		assert '"sample_count": 0' in rv.data
		rv = self.app.post('/ngssm/api/v1.0/samples', data='{"run_id":"1"}', headers=hc)
		assert 'samples/1' in rv.data

		# delete sample
		rv = self.app.delete('/ngssm/api/v1.0/samples/1', headers=h)
		print rv.data
		assert '"result": true' in rv.data

		# verify delete
		rv = self.app.get('/ngssm/api/v1.0/samples', headers=h)
		print rv.data
		assert '"sample_count": 0' in rv.data

	def test_sample_list_retrieve_empty(self):
		"""Test retrieving a sample from an empty list"""
		h = self.get_headers(False)
		rv = self.app.get('/ngssm/api/v1.0/samples/1', headers=h)
		print rv.data
		assert '"status": 404' in rv.data

	def test_sample_list_filter(self):
		"""Test filtering a sample list"""
		h = self.get_headers(False)
		hc = self.get_headers(True)

                # add required run
                rv = self.app.get('/ngssm/api/v1.0/runs', headers=h)
                print rv.data
                assert '"run_count": 0' in rv.data
                rv = self.app.post('/ngssm/api/v1.0/runs', data='{"plate":"5.1"}', headers=hc)
                print rv.data
                assert 'runs/1' in rv.data

		# add sample
		rv = self.app.get('/ngssm/api/v1.0/samples', headers=h)
		print rv.data
		assert '"sample_count": 0' in rv.data
		rv = self.app.post('/ngssm/api/v1.0/samples', data='{"run_id":"1", "sample":"Sample 1"}', headers=hc)
		assert 'samples/1' in rv.data
		rv = self.app.post('/ngssm/api/v1.0/samples', data='{"run_id":"1", "sample":"Sample 2"}', headers=hc)
		assert 'samples/2' in rv.data
		rv = self.app.get('/ngssm/api/v1.0/samples', headers=h)
		assert '"sample_count": 2' in rv.data
		print "Get: /ngssm/api/v1.0/samples?sample=Sample+1"
		rv = self.app.get('/ngssm/api/v1.0/samples?sample=Sample+1', headers=h)
		assert '"sample_count": 1' in rv.data

	def test_run_require_password(self):
		"""Test access to run list without a password."""
		rv = self.app.get('/ngssm/api/v1.0/runs')
		assert 'Unauthorized access' in rv.data

	def test_run_list_empty_db(self):
		"""Verify that the run count of the empty list is 0."""
		h = self.get_headers(False)
		rv = self.app.get('/ngssm/api/v1.0/runs',headers=h)
		assert '"run_count": 0' in rv.data

	def test_run_add(self):
		"""Verify addition of a run.  Should have id 1 and run count should be 1."""
		h = self.get_headers(False)
		hc = self.get_headers(True)
		rv = self.app.get('/ngssm/api/v1.0/runs', headers=h)
		print rv.data
		assert '"run_count": 0' in rv.data
		rv = self.app.post('/ngssm/api/v1.0/runs', data='{"plate":"5.1"}', headers=hc)
		print rv.data
		assert 'runs/1' in rv.data
		rv = self.app.get('/ngssm/api/v1.0/runs', headers=h)
		print rv.data
		assert '"run_count": 1' in rv.data

	def test_run_update(self):
		"""Verify update of a run."""
		h = self.get_headers(False)
		hc = self.get_headers(True)
		rv = self.app.get('/ngssm/api/v1.0/runs', headers=h)
		assert '"run_count": 0' in rv.data
		rv = self.app.post('/ngssm/api/v1.0/runs', data='{"plate":"5.1"}', headers=hc)
		assert 'runs/1' in rv.data
		assert '"mid_set": ""' in rv.data
		rv = self.app.put('/ngssm/api/v1.0/runs/1', data='{"mid_set":"ASDG"}', headers=hc)
		assert '"mid_set": "ASDG"' in rv.data

	def test_run_update_fail_type(self):
		"""Test assignment of boolean values to Run fields.  PUT handler requires unicode, thus should fail."""
		h = self.get_headers(False)
		hc = self.get_headers(True)
		rv = self.app.get('/ngssm/api/v1.0/runs', headers=h)
		assert '"run_count": 0' in rv.data
		rv = self.app.post('/ngssm/api/v1.0/runs', data='{"plate":"5.1"}', headers=hc)
		assert 'runs/1' in rv.data
		rv = self.app.put('/ngssm/api/v1.0/runs/1', data='{"type":True}', headers=hc)
		print rv.data
		assert 'Bad Request' in rv.data
		rv = self.app.put('/ngssm/api/v1.0/runs/1', data='{"mid_set":True}', headers=hc)
		print rv.data
		assert 'Bad Request' in rv.data
		rv = self.app.put('/ngssm/api/v1.0/runs/1', data='{"plate":True}', headers=hc)
		print rv.data
		assert 'Bad Request' in rv.data
		rv = self.app.put('/ngssm/api/v1.0/runs/1', data='{"sequencing_notes":True}', headers=hc)
		print rv.data
		assert 'Bad Request' in rv.data

	def test_run_delete(self):
		"""Test deleting a run"""
		h = self.get_headers(False)
		hc = self.get_headers(True)
		rv = self.app.get('/ngssm/api/v1.0/runs', headers=h)
		assert '"run_count": 0' in rv.data
		rv = self.app.post('/ngssm/api/v1.0/runs', data='{"plate":"5.1"}', headers=hc)
		assert 'runs/1' in rv.data
		rv = self.app.delete('/ngssm/api/v1.0/runs/1', headers=h)
		print rv.data
		assert '"result": true' in rv.data

	def test_run_delete_cascade(self):
		"""Test deleting a run with associated samples"""
		h = self.get_headers(False)
		hc = self.get_headers(True)

		rv = self.app.get('/ngssm/api/v1.0/runs', headers=h)
		print rv.data
		assert '"run_count": 0' in rv.data

		rv = self.app.post('/ngssm/api/v1.0/runs', data='{"plate":"5.1"}', headers=hc)
		print rv.data
		assert 'runs/1' in rv.data

		# add sample
		rv = self.app.get('/ngssm/api/v1.0/samples', headers=h)
		print rv.data
		assert '"sample_count": 0' in rv.data

		rv = self.app.post('/ngssm/api/v1.0/samples', data='{"run_id":"1"}', headers=hc)
		print rv.data
		assert 'samples/1' in rv.data

		rv = self.app.delete('/ngssm/api/v1.0/runs/1', headers=h)
		print rv.data
		assert '"result": true' in rv.data

		rv = self.app.get('/ngssm/api/v1.0/runs', headers=h)
		print rv.data
		assert '"run_count": 0' in rv.data

		rv = self.app.get('/ngssm/api/v1.0/samples', headers=h)
		print rv.data
		assert '"sample_count": 0' in rv.data


	def test_run_list_retrieve_empty(self):
		"""Test retrieving a run from an empty list"""
		h = self.get_headers(False)
		rv = self.app.get('/ngssm/api/v1.0/runs/1', headers=h)
		print rv.data
		assert '"status": 404' in rv.data

	def test_run_list_filter(self):
		"""Test filtering a run list"""
		h = self.get_headers(False)
		hc = self.get_headers(True)
		rv = self.app.get('/ngssm/api/v1.0/runs', headers=h)
		print rv.data
		assert '"run_count": 0' in rv.data
		rv = self.app.post('/ngssm/api/v1.0/runs', data='{"plate":"5.1"}', headers=hc)
		assert 'runs/1' in rv.data
		rv = self.app.post('/ngssm/api/v1.0/runs', data='{"plate":"5.2"}', headers=hc)
		assert 'runs/2' in rv.data
		rv = self.app.get('/ngssm/api/v1.0/runs', headers=h)
		assert '"run_count": 2' in rv.data
		print "Get: /ngssm/api/v1.0/runs?plate=5.1"
		rv = self.app.get('/ngssm/api/v1.0/runs?plate=5.1', headers=h)
		assert '"run_count": 1' in rv.data




#	def test_make_public_sample(self):
#		"""Test ensures conversion of id to URI and removal of id"""
#		sample = Sample(id=1, plate="45.2")
#		self.assertFalse(hasattr(sample, 'uri'))
#		self.assertTrue(hasattr(sample, 'id'))
#		new_sample = ngssm.make_public_sample(sample)
#		self.assertIsNotNone(new_sample)
#		self.assertTrue(hasattr(new_sample), 'uri')
#		self.assertFalse(hasattr(new_sample), 'id')
