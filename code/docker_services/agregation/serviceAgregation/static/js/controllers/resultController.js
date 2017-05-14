angular.module('BibliographyChecker')
  .controller('resultController', function($scope, $http, $window) {
    $scope.waiting = true;
    $scope.showInfo = false;    

    $scope.$watch("angularInit", function(){
        $http.get("/publisherInfo/" + $scope.pId)
        .then(function(response) {
            $scope.selected = response.data['publisherInfo'];
            $scope.waiting = false;
            $scope.showInfo = true; 
        },
        function(response) {
            $scope.showInfo = false; 
        });
        
        if ($scope.showLen > 0)
        {
            $scope.hideArray = [];
            for (i = 0; i < $scope.showLen; i++)
            {
                $scope.hideArray.push(false);
            }
            
            $scope.show = function(pos)
            {
                $scope.hideArray[pos] = !($scope.hideArray[pos]);
            }
            
            $http.get("/templateInfoExamples/" + $scope.pId)
            .then(function(response) {
                $scope.publishersExample = response.data['templateInfo']['templateList']; 
            },
            function(response) {
                $window.location.href = "/error?message=" +response.data['message'];
            });
        }        
    });    
});