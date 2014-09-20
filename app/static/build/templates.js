angular.module('app').run(['$templateCache', function($templateCache) {
  'use strict';

  $templateCache.put('templates/login.html',
    "<form class=\"form-login\" role=\"form\" name=\"login\" novalidate><input type=\"email\" class=\"form-control form-no-bottom\" placeholder=\"Email address\" ng-model=\"loginService.email\" ng-disabled=\"loginService.pending\" required autofocus> <input type=\"password\" class=\"form-control form-no-top\" placeholder=\"Password\" ng-model=\"loginService.password\" ng-disabled=\"loginService.pending\" required> <button class=\"btn btn-lg btn-primary btn-block\" type=\"submit\" ng-click=\"loginService.login()\" ng-disabled=\"loginService.pending || login.$invalid\">Log In</button> <button class=\"btn btn-lg btn-default btn-block\" type=\"submit\" ng-click=\"go('/signup')\">Sign Up</button></form>"
  );


  $templateCache.put('templates/signup.html',
    "<form class=\"form-signup\" role=\"form\" name=\"signup\" novalidate><input type=\"name\" class=\"form-control\" placeholder=\"Full name\" ng-model=\"loginService.name\" required autofocus> <input type=\"email\" class=\"form-control\" placeholder=\"Email address\" ng-model=\"loginService.email\" required> <input type=\"password\" class=\"form-control form-no-bottom\" placeholder=\"Password\" ng-model=\"loginService.password\" required> <input type=\"password\" class=\"form-control form-no-top\" placeholder=\"Confirm Password\" ng-model=\"loginService.confirmPassword\" required> <button class=\"btn btn-lg btn-primary btn-block\" type=\"submit\" ng-click=\"loginService.signup()\" ng-disabled=\"loginService.pending || signup.$invalid\">Sign Up</button> <button class=\"btn btn-lg btn-default btn-block\" type=\"submit\" ng-click=\"go('/')\">Cancel</button></form>"
  );

}]);
