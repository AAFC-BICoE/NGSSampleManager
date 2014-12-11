function SamplesViewModel(ngssmViewModel) {
	var self = this;
	self.ngssmViewModel = ngssmViewModel;
	self.samplesURI = location.origin.concat("/ngssm/api/v1.0/samples");
	self.samples = ko.observableArray();

	self.ajax = function(uri, method, data) {
		var request = {
			url: uri,
			type: method,
			accepts: "application/json",
			cache: false,
			dataType: 'json',
			data: JSON.stringify(data),
			beforeSend: function (xhr) {
				xhr.setRequestHeader("Authorization", 
					"Basic " + btoa(self.ngssmViewModel.loginViewModel.username + ":" + self.ngssmViewModel.loginViewModel.password));
			},
			error: function(jqXHR) {
				console.log("ajax error " + jqXHR.status);
			}
		};
		if (data !== undefined) {
			request["contentType"] = "application/json";
		}
		return $.ajax(request);
	}

	self.beginSampleAdd = function() {
		$('#sampleAddDialog').modal('show');
	}
	self.add = function(sample) {
		self.ajax(self.samplesURI, 'POST', sample).done(function(data) {
			self.samples.push({
				sff: ko.observable(data.sample.sff),
				target: ko.observable(data.sample.target),
				mid: ko.observable(data.sample.mid),
				mid_set: ko.observable(data.sample.mid_set),
				run_id: ko.observable(data.sample.run_id),
				uri: ko.observable(data.sample.uri),
			});
		});
	}
	self.beginSampleEdit = function(sample) {
		self.ngssmViewModel.editSamplesViewModel.setSample(sample);
		$('#sampleEditDialog').modal('show');
	}
	self.edit = function(sample, data) {
		self.ajax(sample.uri(), 'PUT', data).done(function(res) {
			self.updateSample(sample, res.sample);
		});
	}
	self.updateSample = function(sample, newSample) {
		sample.sff(newSample.sff);
		sample.target(newSample.target);
		sample.mid(newSample.mid);
		sample.mid_set(newSample.mid_set);
		sample.run_id(newSample.run_id);
	}
	self.remove = function(sample) {
		self.ajax(sample.uri(), 'DELETE').done(function() {
			self.samples.remove(sample);
		});
	}
}

function AddSamplesViewModel(ngssmViewModel) {
	var self = this;
	self.ngssmViewModel = ngssmViewModel;
	self.sff = ko.observable();
	self.target = ko.observable();
	self.mid = ko.observable();
	self.mid_set = ko.observable();
	self.run_id = ko.observable();
	
	self.addSample = function() {
		$('#sampleAddDialog').modal('hide');
		self.ngssmViewModel.samplesViewModel.add({
			sff: self.sff(),
			target: self.target(),
			mid: self.mid(),
			mid_set: self.mid_set(),
			run_id: self.run_id(),
		});
		self.sff("");
		self.target("");
		self.mid("");
		self.mid_set("");
		self.run_id("");
	}
}

function EditSamplesViewModel(ngssmViewModel) {
	var self = this;
	self.ngssmViewModel = ngssmViewModel;
	self.sff = ko.observable();
	self.target = ko.observable();
	self.mid = ko.observable();
	self.mid_set = ko.observable();
	self.run_id = ko.observable();
	
	self.setSample = function(sample) {
		self.sample = sample;
		self.sff(sample.sff());
		self.target(sample.target());
		self.mid(sample.mid());
		self.mid_set(sample.mid_set());
		self.run_id(sample.run_id());
	}
	self.editSample = function() {
		$('#sampleEditDialog').modal('hide');
		self.ngssmViewModel.samplesViewModel.edit(self.sample, {
			sff: self.sff(),
			target: self.target(),
			mid: self.mid(),
			mid_set: self.mid_set(),
			run_id: self.run_id(),
		});
		self.sff("");
		self.target("");
		self.mid("");
		self.mid_set("");
		self.run_id("");
	}
}

