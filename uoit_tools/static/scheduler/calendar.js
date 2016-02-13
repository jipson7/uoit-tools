
angular.module('uoit-tools')
.directive('calendar', function($timeout) {

    var weekmap = {'M': 1, 'T': 2, 'W': 3, 'R': 4, 'F': 5};

    function addSlot(slot, element, day) {
        var calEvent = {
            start: mergeDayTime(day, slot.start),
            end: mergeDayTime(day, slot.end),
            title: slot.name + ' - ' + slot.type
        }
        $(element).fullCalendar('renderEvent', calEvent, true);
    }

    function mergeDayTime(day, time) {
        var dayStr = day.toLocaleDateString();
        return new Date(dayStr + ' ' + time);
    }

    return {
        restrict: 'A',
        scope: {
            data: '@',
            sunday: '@',
            first: '@'
       },
        link: function($scope, element) {
            var schedule = JSON.parse($scope.data);
            var sunday = new Date($scope.sunday);
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
                defaultDate: sunday
            });
            if ($scope.first) {
                $timeout(function() {
                    $(element).fullCalendar('render');
                });
            }
            
            for (var day in schedule) {
                if (schedule.hasOwnProperty(day)) {
                    var daydate = new Date(sunday.getTime());
                    daydate.setDate(daydate.getDate() + weekmap[day]);
                    var slots = schedule[day];
                    for (var i = 0; i < slots.length; i++) {
                        var slot = slots[i];
                        addSlot(slot, element, daydate);
                    }
                }
            }
        }
    }
});