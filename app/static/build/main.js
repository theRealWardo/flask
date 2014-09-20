var app = angular.module('app', ['ngRoute', 'ui.bootstrap']).config(
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
['$scope',
function($scope) {

  $scope.alerts = [
    /*
    {
      type: 'danger',
      msg: 'Oh snap! Change a few things up and try submitting again.'
    },
    {
      msg: 'Welcome! Hope you like cookies'
    },
    {
      type: 'success',
      msg: 'Well done! You successfully read this important alert message.'
    }
    */
  ];

  $scope.addAlert = function() {
    $scope.alerts.push({msg: 'Another alert!'});
  };

  $scope.closeAlert = function(index) {
    $scope.alerts.splice(index, 1);
  };

}]);


angular.module('app').controller('LoginController',
['$scope', '$location', 'loginService',
function($scope, $location, loginService) {

  $scope.go = function(path) {
    $location.path(path);
  };

  $scope.loginService = loginService;

}]);

app.controller('SignupController',
['$scope', '$location', 'loginService',
function($scope, $location, loginService) {

  $scope.go = function(path) {
    $location.path(path);
  };

  $scope.loginService = loginService;

}]);

angular.module('app').service('loginService', function() {

  this.name = '';
  this.email = '';
  this.password = '';
  this.confirmPassword = '';
  this.pending = false;

  this.login = function() {
    this.pending = true;
  };

  this.signup = function() {
    this.pending = true;
  };

});
