angular.module('app').service('loginService',
['$http', 'alertsService',
function($http, alertsService) {

  this.name = '';
  this.email = '';
  this.password = '';
  this.confirmPassword = '';
  this.pending = false;

  // Successful login will provide these values.
  this.accessToken = null;
  this.refreshToken = null;

  this.login = function() {
    this.pending = true;
    alertsService.clear();
    $http.post('/webauth/signin', {
        email: this.email,
        password: this.password
    }).
    success(angular.bind(this, this.onLogin)).
    error(angular.bind(this, this.onError));
  };

  this.onLogin = function(data, status, headers, config) {
    this.pending = false;
    if (data['access_token']) {
      this.accessToken = data['access_token'];
      this.refreshToken = data['refresh_token'];
    } else {
      alertsService.danger(data['error']);
    }
  };

  this.signup = function() {
    this.pending = true;
    alertsService.clear();
    $http.post('/auth/signup', {
        name: this.name,
        password: this.password
    }).
    success(angular.bind(this, this.onSignup)).
    error(angular.bind(this, this.onError));
  };

  this.onSignup = function(data, status, headers, config) {
    this.pending = false;
    if (data['status'] == 'ok') {
      this.login();
    } else {
      alertsService.danger(data['error']);
    }
  };

  this.onError = function(data, status, headers, config) {
    console.log(data);
    this.pending = false;
  };

}]);
