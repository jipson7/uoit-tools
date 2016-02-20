angular.module('uoit-tools')
.controller('roomfinderController', ['$scope', '$http', function($scope, $http) {
    function init() {
        $scope.sortType = 'num';
        $scope.sortReverse = true;
        $('#roomfinder-datetime').datetimepicker({
            defaultDate: new Date(),
            stepping: 30,
            format: "dddd, MMMM Do YYYY, h:mm a"
        });
    }


    $scope.roomFind = function() {
        $scope.rooms = null;
        $scope.error = null;
        $('#roomFinderSubmit').prop('disabled', true);
        $http({
            url: '/roomfinder',
            method: 'GET',
            params :{ 'date': $('#roomfinder-datetime').data('date') }
        }).then(function(result) {
            var rooms = result.data.rooms;
            if (rooms.length === 0) {
                $scope.error = 'No data available for this date, try a date in the current semester.';
            } else {
                $scope.rooms = rooms;
            }
        }).catch(function(error) {
            $scope.error = 'Unable to contact server, try again later.';
        }).then(function() {
            $('#roomFinderSubmit').prop('disabled', false);
        });
    }

    init();
}])
.directive('roomfinder', function() {
    return {
        restrict: 'E',
        templateUrl: 'static/roomfinder/roomfinder.html',
        controller: 'roomfinderController'
    }
});

