function LoginViewModel() {
	var self = this;
	self.username = ko.observable();
	self.password = ko.observable();

	self.observable = new Observable(self);
	
	self.login = function() {
		$('#login').modal('hide');
		self.login(self.username(),self.password());
	}

	self.beginLogin = function() {
		username = getCookie("username");
		password = getCookie("password");
		if (username.length > 0 || password.length > 0) 
		{
			self.login(username, password);
		} 
		else 
		{
			$('#login').modal('show');
		}
	}

	self.login = function(username, password) {

		self.username = username;
		self.password = password;

		document.cookie = "username= " + username + ";";
		document.cookie = "password= " + password + ";";

		self.notifyObservers('LOGIN_COMPLETE');
	}
}

function getCookie(cname)
		{
			var name = cname + "=";
			var ca = document.cookie.split(';');
			for(var i=0; i<ca.length; i++) 
			{
				var c = ca[i].trim();
				if (c.indexOf(name)==0) return c.substring(name.length,c.length);
			}
			return "";
		}

