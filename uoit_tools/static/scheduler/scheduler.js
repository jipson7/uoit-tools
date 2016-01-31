
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

    function init() {
        $scope.schedule = {};
        var classTip = 'Enter a list of comma separated course codes.';
        $('#classList').tooltip({
            'trigger':'focus',
            'title': classTip, 
            'placement':'bottom'
        });
    }

    $scope.submitSchedule = function() {
        var courses = $scope.schedule.courses;
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
        }
        console.log(validCourses);
    };

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

    init();
}])
.directive('scheduler', function() {
    return {
        restrict: 'E',
        templateUrl: 'static/scheduler/scheduler.html',
        controller: 'schedulerController'
    }
});
