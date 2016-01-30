angular.module('uoit-tools')
.controller('roomfinderController', ['$scope', function($scope) {
    function init() {
        $('#roomfinder-datetime').datetimepicker({
            defaultDate: new Date(),
            stepping: 30,
            format: "dddd, MMMM Do YYYY, h:mm a"
        });
    }


    $scope.roomFind = function() {
        var date = $('#roomfinder-datetime').data('date');
        $.ajax({
            url: '/roomfinder',
            data: { 'date': date },
            success: displayRooms,
            error: showRoomFinderError
        });
    }


    function displayRooms(result) {
        var table = $('#roomfinder-table')
            .html('<thead><tr><th>Room</th><th>Available Until</th></tr></thead>');
        rooms = result.rooms;
        for (var key in rooms) {
            if(rooms.hasOwnProperty(key)) {
                var available = (rooms[key] == null) ? 'End of Day' : rooms[key]
                table.append('<tr><td>' + key + '</td><td>' + available + '</td</tr>');
            }
        }
    }

    function showRoomFinderError(error) {
        console.log('fail');
        console.log(error);
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

