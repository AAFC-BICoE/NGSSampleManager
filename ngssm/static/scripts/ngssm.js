function NgssmViewModel() {
	var self = this;

	self.folders = ['runs', 'samples']
	self.chosenFolderId = ko.observable();

	self.goToFolder = function(folder) { 
		self.chosenFolderId(folder); 
		$('#runContainer')[0].style.display = 'none';
		$('#sampleContainer')[0].style.display = 'none';
		if (folder == "runs") {
			$('#runContainer')[0].style.display = 'block';
		} else if (folder = "samples") {
			$('#sampleContainer')[0].style.display = 'block';
		}
		self.refreshViewModels();
	};

	self.loginViewModel = new LoginViewModel();
	self.samplesViewModel = new SamplesViewModel(self.loginViewModel);
	self.addSamplesViewModel = new AddSamplesViewModel(self.loginViewModel);
	self.editSamplesViewModel = new EditSamplesViewModel(self.loginViewModel);
	self.runsViewModel = new RunsViewModel(self.loginViewModel);
	self.addRunsViewModel = new AddRunsViewModel(self.loginViewModel);
	self.editRunsViewModel = new EditRunsViewModel(self.loginViewModel);

	ko.applyBindings(self.loginViewModel, $('#loginDialog')[0]);
	ko.applyBindings(self.samplesViewModel, $('#sampleContainer')[0]);
	ko.applyBindings(self.addSamplesViewModel, $('#sampleAddDialog')[0]);
	ko.applyBindings(self.editSamplesViewModel, $('#sampleEditDialog')[0]);
	ko.applyBindings(self.runsViewModel, $('#runContainer')[0]);
	ko.applyBindings(self.addRunsViewModel, $('#runAddDialog')[0]);
	ko.applyBindings(self.editRunsViewModel, $('#runEditDialog')[0]);

	self.loginViewModel.beginLogin();

	self.refreshViewModels = function() {
		if (self.chosenFolderId() == "samples") {
			self.refreshSamplesViewModel();
		} else if (self.chosenFolderId() == "runs") {
			self.refreshRunsViewModel();
		} else {
			alert ("Failed to refresh unsupported view model: " + self.chosenFolderId());
		}
	}

	self.refreshRunsViewModel = function() {
		self.runsViewModel.ajax(self.runsViewModel.runsURI, 'GET').done(function(tempdata) {
			self.runsViewModel.runs.removeAll();
			for (var i = 1; i <= tempdata.runs.length; i++) {
				self.runsViewModel.ajax(self.runsViewModel.runsURI.concat('/', i), 'GET').done(function(data) {
					self.runsViewModel.runs.push({
						uri: ko.observable(data.run.uri),
						mid_set: ko.observable(data.run.mid_set),
						plate: ko.observable(data.run.plate),
						type: ko.observable(data.run.type),
					});
				}).fail(function(jqXHR) {
					if(jqXHR.status = 403) {
						setTimeout(self.beginLogin, 500);
					}
				});
			}
		}).fail(function(jqXHR) {
			if(jqXHR.status = 403) {
				setTimeout(self.beginLogin, 500);
			}
		});
	}

	self.refreshSamplesViewModel = function() {
		self.samplesViewModel.ajax(self.samplesViewModel.samplesURI, 'GET').done(function(data) {
			self.samplesViewModel.samples.removeAll();
			for (var i = 0; i < data.samples.length; i++) {
				self.samplesViewModel.samples.push({
					uri: ko.observable(data.samples[i].uri),
					sff: ko.observable(data.samples[i].sff),
					target: ko.observable(data.samples[i].target),
					mid: ko.observable(data.samples[i].mid),
					mid_set: ko.observable(data.samples[i].mid_set),
					run_id: ko.observable(data.samples[i].run_id),
				});
			}
		}).fail(function(jqXHR) {
			if(jqXHR.status = 403) {
				setTimeout(self.beginLogin, 500);
			}
		});
	}

	// TODO refreshing the list is slow; maybe delete only affected entries (or look at performance of filling list)?
	self.loginViewModel.registerObserver(new Observer(self.refreshViewModels));

	self.goToFolder('runs');
}
