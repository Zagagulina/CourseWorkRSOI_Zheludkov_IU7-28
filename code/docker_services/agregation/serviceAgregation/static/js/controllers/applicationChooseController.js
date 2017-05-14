angular.module('BibliographyChecker')
  .controller('applicationChooseController', function($scope, $http, $window) {
    $scope.waiting = true;
    
    $scope.$watch("applicationChooseInit", function(){
        $scope.show = false;
        $http.get("/application")
            .then(function(response) {
                if (response.data['appList'] != 'none')
                {
                    $scope.appList = response.data['appList'];
                    $scope.appList.splice(0, 1);
                    if ($scope.appList.length != 0)
                    {
                        $scope.selected = $scope.appList[0];
                        $scope.show = true;
                    }
                    $scope.size = Math.min($scope.appList.length, 7);                    
                }    
                $scope.waiting = false;
            },
            function(response) {
                $window.location.href = "/error?message=" +response.data['message'];
            });            
    })
});