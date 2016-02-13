
angular.module('uoit-tools')
.directive('calendar', function() {
    return {
        restrict: 'A',
        scope: {
            data: '@',
            sunday: '@'
       },
        link: function($scope, element) {
            $(element).fullCalendar({
                header: {
                    left: '',
                    center: '',
                    right: ''
                },
                defaultView: 'agendaWeek',
                allDaySlot: false,
                minTime: '08:00:00',
                maxTime: '22:00:00',
                weekends: false,
                height: 'auto',
                columnFormat: 'ddd',
                defaultDate: $scope.sunday
            });
        }
    }
});
