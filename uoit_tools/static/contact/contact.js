
angular.module('uoit-tools')
.controller('contactController', ['$scope', '$http', function($scope, $http) {

}])
.directive('contact', function() {
    return {
        restrict: 'E',
        templateUrl: 'static/contact/contact.html',
        controller: 'contactController'
    }
});
