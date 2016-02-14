
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

    (function initForm() {
        $scope.schedule = {};
        var classTip = 'Enter a list of comma separated course codes.';
        $('#classList').tooltip({
            'trigger':'focus',
            'title': classTip, 
            'placement':'top'
        });
    })();

    $(document).on('shown.bs.tab', 'a[data-toggle="tab"]', function (e) {
        var target = $(e.target).attr("href");
        $(target).fullCalendar('render');
    })


    $scope.submitSchedule = function() {
        delete $scope.schedules;
        var courses = $scope.schedule.courses;
        $scope.error = null
        if (!courses || !courses.length) {
            $scope.error = 'Must provide at least one course...';
            return;
        }
        var invalid = []
        var valid = []
        for (var i in courses) {
            var course = cleanCourse(courses[i]);
            if (!course) {
                invalid.push(courses[i])
            } else {
                valid.push(course);
            }
        }
        if (invalid.length) {
            $scope.error = 'The following courses are invalid: ' + invalid.join(', ');
        } else {
            $scope.schedule.courses = valid;
            postData();
        }
    };

    function postData() {
        $('#generate').prop('disabled', true)
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
        }).catch(function(error) {
            if (error.status === 500)
                $scope.error = 'Unable to contact server, try again later...';
            else
                $scope.error = error.data;
        }).then(function() {
            $('#generate').prop('disabled', false)
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
