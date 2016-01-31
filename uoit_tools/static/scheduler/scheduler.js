
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
            //fetchSemesters();        
        });
    })();

    function init() {
        $scope.schedule = {};
    }

    $scope.submitSchedule = function() {
        console.log($scope.schedule);
    };

    init();
}])
.directive('scheduler', function() {
    return {
        restrict: 'E',
        templateUrl: 'static/scheduler/scheduler.html',
        controller: 'schedulerController'
    }
});
