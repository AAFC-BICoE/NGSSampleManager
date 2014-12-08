function RunsViewModel(ngssmViewModel) {
	var self = this;
	self.ngssmViewModel = ngssmViewModel;
	self.runsURI = location.origin.concat("/ngssm/api/v1.0/runs");
	self.runs = ko.observableArray();

	self.observable = new Observable(self);

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


	self.beginRunAdd = function() {
		$('#runAddDialog').modal('show');
	}
	self.add = function(run) {
		self.ajax(self.runsURI, 'POST', run).done(function(data) {
			self.runs.push({
				mid_set: ko.observable(data.run.mid_set),
				plate: ko.observable(data.run.plate),
				type: ko.observable(data.run.type),
				uri: ko.observable(data.run.uri),
			});
		});
	}
	
	self.beginRunEdit = function(run) {
		self.ngssmViewModel.editRunsViewModel.setRun(run);
		$('#runEditDialog').modal('show');
	}
	self.edit = function(run, data) {
		self.ajax(run.uri(), 'PUT', data).done(function(res) {
			self.updateRun(run, res.run);
		});
	}
	self.updateRun = function(run, newRun) {
		var i = self.runs.indexOf(run);
		self.runs()[i].plate(newRun.plate);
		self.runs()[i].mid_set(newRun.mid_set);
		self.runs()[i].type(newRun.type);
	}
	self.remove = function(run) {
		self.ajax(run.uri(), 'DELETE').done(function() {
			self.runs.remove(run);
			self.notifyObservers('DELETE');
		});
	}
}

function AddRunsViewModel(ngssmViewModel) {
	var self = this;
	self.ngssmViewModel = ngssmViewModel;
	self.plate = ko.observable();
	self.mid_set = ko.observable();
	self.type = ko.observable();
	
	self.addRun = function() {
		$('#runAddDialog').modal('hide');
		self.ngssmViewModel.runsViewModel.add({
			plate: self.plate(),
			mid_set: self.mid_set(),
			type: self.type(),
		});
		self.plate("");
		self.mid_set("");
		self.type("");
	}
}

function EditRunsViewModel(ngssmViewModel) {
	var self = this;
	self.ngssmViewModel = ngssmViewModel;
	self.plate = ko.observable();
	self.mid_set = ko.observable();
	self.type = ko.observable();

	self.setRun = function(run) {
		self.run = run;
		self.plate(run.plate());
		self.mid_set(run.mid_set());
		self.type(run.type());
	}
	self.editRun = function() {
		$('#runEditDialog').modal('hide');
		self.ngssmViewModel.runsViewModel.edit(self.run, {
			plate: self.plate(),
			mid_set: self.mid_set(),
			type: self.type(),
		});
		self.plate("");
		self.mid_set("");
		self.type("");
	}
}

//var samplesViewModel = new SamplesViewModel();
//var addSamplesViewModel = new AddSamplesViewModel();
//var editSamplesViewModel = new EditSamplesViewModel();

//var runsViewModel = new RunsViewModel();
//var addRunsViewModel = new AddRunsViewModel();
//var editRunsViewModel = new EditRunsViewModel();

//var loginViewModel = new LoginViewModel();
//window.alert(loginViewModel)
