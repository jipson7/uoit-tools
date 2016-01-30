
angular.module('uoit-tools')
.controller('schedulerController', ['$scope', '$http', function($scope, $http) {
    $scope.testdata ='WORKROKROWKEOWKE';
}])
.directive('scheduler', function() {
    return {
        restrict: 'E',
        templateUrl: 'static/scheduler/scheduler.html',
        controller: 'schedulerController'
    }
});
