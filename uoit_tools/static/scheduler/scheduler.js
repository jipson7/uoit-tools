
angular.module('uoit-tools')
.controller('schedulerController', ['$scope', '$http', function($scope, $http) {
    (function fetchSemesters() {
        $http({
            'url': '/scheduler/semesters',
            'method': 'GET'
        }).then(function(result) {
            $scope.semesters = result.data.semesters;
            $scope.schedule.semester = result.data.current;
        }).catch(function(error) {
            console.log('Unable to fetch semester list. Retrying...');
            fetchSemesters();        
        });
    })();

    (function init() {
        $scope.schedule = {};
        var classTip = 'Enter a list of comma separated course codes.';
        $('#classList').tooltip({
            'trigger':'focus',
            'title': classTip, 
            'placement':'bottom'
        });
    })();

    function displaySchedulingErrors(errors) {
        for (var i = 0; i < errors.length; i++) {
            console.log(errors[i]);
        }
    }

    function createSlides(result) {
        var schedules = result.data.schedules;
        var sunday = result.data.firstSunday;
        displaySchedulingErrors(result.data.errors);

        $scope.tabs = []

        for (var i = 1; i <= schedules.length; i++) {
            $scope.tabs.push(i);
            var id = 'schedule-' + i
            var schedule = schedules[i];
            createCalendar(schedule, sunday, id);
        }

        $(function() {
            $('#schedule-slides a').click(function (e) {
                e.preventDefault()
                $(this).tab('show')
            })
        });
    }

    function createCalendar(schedule, sunday, id) {
        var calendar = $('<div/>')
        calendar.fullCalendar({
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
        console.log($('#' + id).length)
    }

    $scope.submitSchedule = function() {
        var courses = $scope.schedule.courses;
        if (!courses) {
            $scope.courseListError = 'Must provide at least one course...'
                return
        }
        $scope.courseListError = null;
        invalidCourses = [];
        validCourses = []
        for (var i in courses) {
            var course = cleanCourse(courses[i]);
            if (!course) {
                invalidCourses.push(courses[i]); 
            } else {
                validCourses.push(course);
            }
        }
        if (invalidCourses.length) {
            $scope.courseListError = 'The following course codes are invalid: ' 
                + invalidCourses.join(', ');
        } else {
            $scope.schedule.courses = validCourses;
            postData();
        }
    };

    function postData() {
        $http({
            'url': '/scheduler',
            'method': 'POST',
            'data': $.param($scope.schedule),
            'headers': {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        }).then(function(result) {
            createSlides(result);
        }).catch(function(error) {
            $scope.courseListError = 'Unable to contact server, try again later...';
        });
    }

    function cleanCourse(course) {
        course = course.replace(/\s/g, '').toUpperCase();
        var deptRE = /^([A-Z]{3,4})/;
        var codeRE = /([0-9]{4})/;
        var dept = deptRE.exec(course);
        var code = codeRE.exec(course);
        if (!dept || !code) {
            return false;
        } else {
            dept = dept[0];
            code = code[0];
        }
        var year = parseInt(code.charAt(0));
        if (year < 5) {
            code += 'U';
        } else {
            code += 'G';
        }
        return (dept + code);
    }
}])
.directive('scheduler', function() {
    return {
        restrict: 'E',
        templateUrl: 'static/scheduler/scheduler.html',
        controller: 'schedulerController'
    }
});
