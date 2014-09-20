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
