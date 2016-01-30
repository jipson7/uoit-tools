
angular.module('uoit-tools')
.controller('contactController', ['$scope', '$http', function($scope, $http) {
    $scope.submitForm = function(isValid) {
        if (isValid) {
            console.log('submitting valid form')
        }
    }
}])
.directive('contact', function() {
    return {
        restrict: 'E',
        templateUrl: 'static/contact/contact.html',
        controller: 'contactController'
    }
});
