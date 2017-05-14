angular.module('BibliographyChecker')
  .controller('checkController', function($scope, $http, $window) {
    $scope.waiting = true;
        
    $http.get("/publishersModerated")
        .then(function(response) {
            $scope.PublishersList = response.data['publishers'];
            $scope.selected = $scope.PublishersList[0];
            $scope.size = Math.min($scope.PublishersList.length, 7);
            $scope.waiting = false;
        },
        function(response) {
            $window.location.href = "/error?message=" +response.data['message'];
        });
        
    $scope.bibliography = "";
      
    $scope.trueWaiting = function() {
        $scope.waiting = true;
    }        
      
    $scope.postData = function() {
        if ($scope.bibliography.length == 0)
        {
            return;
        }

        $scope.waiting = true;
        
        var data = {
                bibliography: $scope.bibliography,
                selectedPublisher: $scope.selected.id
            };        
        $http.post("/validateBibliography", data)
              .then(function(response) {
                  $window.location.href = "/main";
                  $scope.waiting = false;
              },
              function(response) {
                  $window.location.href = "/error?message=" +response.data['message'];
              })
    };
});