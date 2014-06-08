function SamplesViewModel(loginViewModel) {
	var self = this;
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
					"Basic " + btoa(loginViewModel.username + ":" + loginViewModel.password));
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

	self.beginAdd = function() {
		$('#add').modal('show');
	}
	self.add = function(sample) {
		self.ajax(self.samplesURI, 'POST', sample).done(function(data) {
			self.samples.push({
				sff: ko.observable(data.sample.sff),
				target: ko.observable(data.sample.target),
				mid: ko.observable(data.sample.mid),
				mid_set: ko.observable(data.sample.mid_set),
				run: ko.observable(data.sample.run),
				uri: ko.observable(data.sample.uri),
			});
		});
	}
	
	self.beginEdit = function(sample) {
		editSamplesViewModel.setSample(sample);
		$('#edit').modal('show');
	}
	self.edit = function(sample, data) {
		self.ajax(sample.uri(), 'PUT', data).done(function(res) {
			self.updateSample(sample, res.sample);
		});
	}
	self.updateSample = function(sample, newSample) {
		var i = self.samples.indexOf(sample);
		self.samples()[i].sff(newSample.sff);
		self.samples()[i].target(newSample.target);
		self.samples()[i].mid(newSample.mid);
		self.samples()[i].mid_set(newSample.mid_set);
		self.samples()[i].run(newSample.run);
	}

	self.remove = function(sample) {
		self.ajax(sample.uri(), 'DELETE').done(function() {
			self.samples.remove(sample);
		});
	}
	
}

function AddSamplesViewModel() {
	var self = this;
	self.sff = ko.observable();
	self.target = ko.observable();
	self.mid = ko.observable();
	self.mid_set = ko.observable();
	self.run= ko.observable();
	
	self.addSample = function() {
		$('#add').modal('hide');
		samplesViewModel.add({
			sff: self.sff(),
			target: self.target(),
			mid: self.mid(),
			mid_set: self.mid_set(),
			run: self.run(),
		});
		self.sff("");
		self.target("");
		self.mid("");
		self.mid_set("");
		self.run("");
	}
}

function EditSamplesViewModel() {
	var self = this;
	self.sff = ko.observable();
	self.target = ko.observable();
	self.mid = ko.observable();
	self.mid_set = ko.observable();
	self.run= ko.observable();
	
	self.setSample = function(sample) {
		self.sample = sample;
		self.sff(sample.sff());
		self.target(sample.target());
		self.mid(sample.mid());
		self.mid_set(sample.mid_set());
		self.run(sample.run());
	}
	self.editSample = function() {
		$('#edit').modal('hide');
		samplesViewModel.edit(self.sample, {
			sff: self.sff(),
			target: self.target(),
			mid: self.mid(),
			mid_set: self.mid_set(),
			run: self.run(),
		});
		self.sff("");
		self.target("");
		self.mid("");
		self.mid_set("");
		self.run("");
	}
}
