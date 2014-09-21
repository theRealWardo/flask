describe('LoginService', function() {
  beforeEach(module('app'));

  var alertsService, loginService, httpBackend;
  beforeEach(inject(function(_alertsService_, _loginService_, $httpBackend) {
    alertsService = _alertsService_;
    loginService = _loginService_;
    httpBackend = $httpBackend;
  }));

  var loginRequestJson = {
    email: 'test@test.com',
    password: 'test'
  };
  var loginResponseJson = {
    access_token: 'pbCrFzSU7xZiUtddWCxlI20NAcF5yd',
    token_type: 'Bearer',
    refresh_token: 'u4zwPunL1c38UKloX82tYKKyI8HWt8',
    scope: 'email'
  };
  var loginResponseErrorJson = {
    'error': 'Invalid email or password.', 
    'status': 'error'
  };

  verifyLogin = function(l) {
    expect(l.pending).toBe(false);
    expect(l.accessToken).not.toBeNull();
    expect(l.refreshToken).not.toBeNull();
  };


  describe('when logging in', function() {
    it('posts data and handles an ok response', function() {
      httpBackend.
        expectPOST(
            '/webauth/signin',
            JSON.stringify(loginRequestJson)).
        respond(
            200,
            JSON.stringify(loginResponseJson));
      loginService.email = 'test@test.com';
      loginService.password = 'test';
      loginService.login()
      expect(loginService.pending).toBe(true);
      httpBackend.flush();
      verifyLogin(loginService);
    });

    it('posts data and handles an error response', function() {
      httpBackend.
        expectPOST(
            '/webauth/signin',
            JSON.stringify(loginRequestJson)).
        respond(
            200,
            JSON.stringify(loginResponseErrorJson));
      loginService.email = 'test@test.com';
      loginService.password = 'test';
      loginService.login()
      expect(loginService.pending).toBe(true);
      expect(alertsService.alerts.length).toBe(0);
      httpBackend.flush();
      expect(loginService.pending).toBe(false);
      expect(alertsService.alerts.length).toBe(1);
    });
  });

});
