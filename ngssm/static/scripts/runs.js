function RunsViewModel(ngssmViewModel) {
	var self = this;
	self.ngssmViewModel = ngssmViewModel;
	self.runsURI = location.origin.concat("/ngssm/api/v1.0/runs");
	self.runs = ko.observableArray();

	self.observable = new Observable(self);

	self.beginRunAdd = function() {
		$('#runAddDialog').modal('show');
	}
	self.add = function(run) {
		self.ngssmViewModel.ajax(self.runsURI, 'POST', run).done(function(data) {
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
	
	self.remove = function(run) {
		self.ngssmViewModel.ajax(run.uri(), 'DELETE').done(function() {
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

	self.edit = function(run, data) {
		self.ngssmViewModel.ajax(run.uri(), 'PUT', data).done(function(res) {
			self.updateRun(run, res.run);
		});
	}

	self.updateRun = function(run, newRun) {
		run.plate(newRun.plate);
		run.mid_set(newRun.mid_set);
		run.type(newRun.type);
	}
	
	self.setRun = function(run) {
		self.run = run;
		self.plate(run.plate());
		self.mid_set(run.mid_set());
		self.type(run.type());
	}

	self.editRun = function() {
		$('#runEditDialog').modal('hide');
		self.edit(self.run, {
			plate: self.plate(),
			mid_set: self.mid_set(),
			type: self.type(),
		});
		self.plate("");
		self.mid_set("");
		self.type("");
	}
}
