function Observable(model) {
	var self = this;
	self.observers = [];
	var model = model;

	model.registerObserver = function (observer) {
		// TODO ensure observer implements Observer
		self.observers.push(observer);
	}
	model.unregisterObserver = function (observer) {
		var index = self.observers.indexOf(observer);
		if (index > -1) {
			self.observers.splice(index,1);
		}
	}
	model.notifyObservers = function(e) {
		var len = self.observers.length;
		for (var i = 0; i < len; i++) {
			self.observers[i].notify(e);
		}
	}
}

function Observer(notifyCallback) {
	var self = this;
	
	self.notify = function (e) {
		notifyCallback(e);
	}
}	
