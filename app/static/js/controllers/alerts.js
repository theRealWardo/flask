angular.module('app').controller('AlertDemoCtrl',
['$scope', 'alertsService',
function($scope, alertsService) {

  $scope.alerts = alertsService.alerts;

}]);
