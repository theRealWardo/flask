angular.module('app', ['ngRoute', 'ui.bootstrap']).config(
['$routeProvider',
function($routeProvider) {

  $routeProvider.
      when('/login', {
        templateUrl: 'templates/login.html',
        controller: 'LoginController'
      }).
      when('/signup', {
        templateUrl: 'templates/signup.html',
        controller: 'SignupController'
      }).
      otherwise({
        redirectTo: '/login'
      });

}]);

angular.module('app').controller('AlertDemoCtrl',
['$scope', 'alertsService',
function($scope, alertsService) {

  $scope.alerts = alertsService.alerts;

}]);

angular.module('app').controller('LoginController',
['$scope', '$location', 'loginService',
function($scope, $location, loginService) {

  $scope.go = function(path) {
    $location.path(path);
  };

  $scope.loginService = loginService;

}]);

angular.module('app').controller('SignupController',
['$scope', '$location', 'loginService',
function($scope, $location, loginService) {

  $scope.go = function(path) {
    $location.path(path);
  };

  $scope.loginService = loginService;

}]);


angular.module('app').service('alertsService',
function() {

  this.alerts = [];

  this.clear = function() {
    // Angular holds a deep reference to the array so we need to work
    // with that object. Clear via popping all the alerts out of the array.
    while (this.alerts.length) {
      this.alerts.pop();
    }
  };

  this.danger = function(message) {
    this.alerts.push({
      type: 'danger',
      msg: message
    });
  };

  this.success = function(message) {
    this.alerts.push({
      type: 'success',
      msg: message
    });
  };

  this.add = function(message) {
    this.alerts.push({
      msg: message
    });
  };

});

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
