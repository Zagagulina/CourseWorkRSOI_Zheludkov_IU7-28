angular.module('BibliographyChecker')
  .controller('publisherInfoController', function($scope, $http, $window) {
    $scope.showInfo = false;    

    $scope.$watch("angularInitPublisher", function(){
        $scope.error = false; 
        $http.get("/publisherInfo/" + $scope.pId)
        .then(function(response) {
            $scope.selected = response.data['publisherInfo'];
            $scope.showInfo = true; 
        },
        function(response) {
            $scope.error = true;
        });        
    });    
});