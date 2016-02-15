
angular.module('uoit-tools')
.controller('contactController', ['$scope', '$http', function($scope, $http) {
    $scope.submitForm = function(form) {
        if (form.$valid) {
            $http({
                'url': '/contact',
                'method': 'POST',
                'data': $.param($scope.contact),
                'headers': {
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
            }).then(function(result) {
                $scope.successMessage = result.data;
                delete $scope.contact;
                form.$setPristine();
            }).catch(function(error) {
                $scope.errorMessage = error.data;
            });
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
