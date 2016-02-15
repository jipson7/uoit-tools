
angular.module('uoit-tools')
.directive('calendar', ['$timeout', 'ngDialog', function($timeout, ngDialog) {

    var weekmap = {'M': 1, 'T': 2, 'W': 3, 'R': 4, 'F': 5};

    function createEvent(slot, day) {
        return {
            start: mergeDayTime(day, slot.start),
            end: mergeDayTime(day, slot.end),
            title: slot.name + ' - ' + slot.type,
            regCodes: slot.reg
        }
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
            var events = [];

            for (var day in schedule) {
                if (schedule.hasOwnProperty(day)) {
                    var daydate = new Date(sunday.getTime());
                    daydate.setDate(daydate.getDate() + weekmap[day]);
                    var slots = schedule[day];
                    for (var i = 0; i < slots.length; i++) {
                        var slot = slots[i];
                        events.push(createEvent(slot, daydate));
                    }
                }
            }

            $(element).fullCalendar({
                customButtons: {
                    register: {
                        text: 'How to Register for this Schedule',
                        click: function() {
                            ngDialog.open({
                                template: '/static/scheduler/register.html',
                                controller: 'registerController',
                                data: {'events': events}
                            });
                        }
                    },
                    prevSchedule: {
                        text: 'Previous',
                        click: function() {
                            $('.nav-tabs > .active').prev('li')
                                .find('a').trigger('click');
                        }
                    },
                    nextSchedule: {
                        text: 'Next',
                        click: function() {
                            $('.nav-tabs > .active').next('li')
                                .find('a').trigger('click');
                        }
                    }
                },
                header: {
                    left: 'prevSchedule',
                    center: 'register',
                    right: 'nextSchedule'
                },
                defaultView: 'agendaWeek',
                allDaySlot: false,
                minTime: '08:00:00',
                maxTime: '22:00:00',
                weekends: false,
                height: 'auto',
                columnFormat: 'ddd',
                defaultDate: sunday,
                events: events,
                eventRender: function(event, element) {
                    element.tooltip({
                        title: event.title
                    })
                }
            });
            
            
            if ($scope.first) {
                $timeout(function() {
                    $(element).fullCalendar('render');
                });
            }
            $('.fc-button').removeClass().addClass('btn btn-default');
        }
    }
}]);
