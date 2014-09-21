describe('AlertsService', function() {
  beforeEach(module('app'));

  var alertsService;
  beforeEach(inject(function(_alertsService_) {
    alertsService = _alertsService_;
  }));

  describe('when adding alerts', function() {
    it('puts them in the array', function() {
      var array = alertsService.alerts;
      alertsService.add('test');
      expect(array.length).toBe(1);
      alertsService.danger('d');
      expect(array.length).toBe(2);
      alertsService.success('s');
      expect(array.length).toBe(3);
    });

    it('clears the referenced array', function() {
      var array = alertsService.alerts;
      for (var i = 0; i < 10; i++) {
        // Throw 10 alerts in there.
        alertsService.add('test');
      }
      alertsService.clear();
      expect(array.length).toBe(0);
    });
  });

});

