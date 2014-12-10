function RunsViewModel(loginViewModel) {
	var self = this;
	self.runsURI = location.origin.concat("/ngssm/api/v1.0/runs");
	self.runs = ko.observableArray().paged(10);
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
		editRunsViewModel.setRun(run);
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

function AddRunsViewModel() {
	var self = this;
	self.plate = ko.observable();
	self.mid_set = ko.observable();
	self.type = ko.observable();
	
	self.addRun = function() {
		$('#runAddDialog').modal('hide');
		runsViewModel.add({
			plate: self.plate(),
			mid_set: self.mid_set(),
			type: self.type(),
		});
		self.plate("");
		self.mid_set("");
		self.type("");
	}
}

function EditRunsViewModel() {
	var self = this;
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
		runsViewModel.edit(self.run, {
			plate: self.plate(),
			mid_set: self.mid_set(),
			type: self.type(),
		});
		self.plate("");
		self.mid_set("");
		self.type("");
	}
}

ko.observableArray.fn.paged = function (perPage, sortComparator) {
    var items = this;

    items.currentPage = ko.observable();
            items.pageSize = ko.observable(perPage);
            items.currentPageIndex = ko.observable(0);

            items.currentItemPage = ko.computed(function () {
                var pagesize = parseInt(items.pageSize(), 10),
                    startIndex = pagesize * items.currentPageIndex(),
                    endIndex = startIndex + pagesize;
                return this().slice(startIndex, endIndex);
            }, items);

            items.pagedItems = ko.computed(function () {
                var size = parseInt(items.pageSize(), 10),
                    start = items.currentPageIndex() * size;

                if (typeof (sortComparator) === "function") {
                    var sorted = this().sort(sortComparator);
                    return sorted.slice(start, start + size);
                } else {
                    return this().slice(start, start + size);
                }


            }, items);

            items.maxPageIndex = ko.computed(function () {
                return Math.ceil(this().length / items.pageSize()) - 1;
            }, items);

            items.allPages = ko.computed(function () {
                var pages = [];
                for (var i = 0; i <= items.maxPageIndex() ; i++) {
                    pages.push({ pageNumber: (i + 1) });
                }
                return pages;
            }, items);

            items.currentStatus = ko.computed(function () {
                var pagesize = parseInt(items.pageSize(), 10),
                    start = pagesize * items.currentPageIndex(),
                    end = start + pagesize;

                if (items.currentPageIndex() === items.maxPageIndex()) end = this().length;

                return 'Showing ' + (start + 1) + ' to ' + end + ' of ' + this().length;
            }, items);

            items.nextPage = function () {
                if (((items.currentPageIndex() + 1) * items.pageSize()) < items().length) {                 
                    items.currentPageIndex(items.currentPageIndex() + 1);
                } else {
                    items.currentPageIndex(0);
                }
            };

            items.previousPage = function () {
                if (items.currentPageIndex() > 0) {
                    items.currentPageIndex(items.currentPageIndex() - 1);
                } else {
                    items.currentPageIndex((Math.ceil(items().length / items.pageSize())) - 1);
                }
            };

            items.moveToPage = function (index) {
                items.currentPageIndex(index);
            };

            return items;
};
