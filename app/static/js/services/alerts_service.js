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
