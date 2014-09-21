angular.module('app').controller('SignupController',
['$scope', '$location', 'loginService',
function($scope, $location, loginService) {

  $scope.go = function(path) {
    $location.path(path);
  };

  $scope.loginService = loginService;

}]);
