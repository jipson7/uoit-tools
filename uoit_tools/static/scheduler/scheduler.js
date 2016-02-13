
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

    $(document).on('shown.bs.tab', 'a[data-toggle="tab"]', function (e) {
        var target = $(e.target).attr("href");
        $(target).fullCalendar('render');
    })

    function displaySchedulingErrors(errors) {
        for (var i = 0; i < errors.length; i++) {
            console.log(errors[i]);
        }
    }

    $scope.submitSchedule = function() {
        var courses = $scope.schedule.courses;
        if (!courses) {
            $scope.courseListError = 'Must provide at least one course...';
            return;
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
            $scope.schedules = result.data.schedules;
            $scope.sunday = result.data.firstSunday;
            displaySchedulingErrors(result.data.errors);
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
