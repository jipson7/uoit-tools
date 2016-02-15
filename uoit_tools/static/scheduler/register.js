
angular.module('uoit-tools')
.controller('registerController', ['$scope', function($scope) {
    var events = $scope.ngDialogData.events;

    var codeList = {};

    for (var i in events) {
        if (events.hasOwnProperty(i)) {
            var event = events[i];
            if (!codeList.hasOwnProperty(event.title)) {
                codeList[event.title] = event.regCodes;
            }
        }
    }

    console.log(codeList);

    $scope.codeList = codeList;
}]);
