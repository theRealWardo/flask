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
