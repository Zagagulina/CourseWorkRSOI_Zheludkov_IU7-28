angular.module('BibliographyChecker')
  .controller('templateChooseController', function($scope, $http, $window) {
    $scope.waiting = true;
    
    $scope.$watch("templateChooseInit", function(){
        $scope.show = false;
        $http.get("/templateInfoFull")
            .then(function(response) {
                if (response.data['templateInfo'] != 'none')
                {
                    $scope.TemplateList = response.data['templateInfo']['templateList'];
                    if ($scope.TemplateList.length != 0)
                    {
                        $scope.selected = $scope.TemplateList[0];
                        $scope.show = true;
                    }
                    $scope.size = Math.min($scope.TemplateList.length, 7);                    
                }    
                $scope.waiting = false;
            },
            function(response) {
                $window.location.href = "/error?message=" +response.data['message'];
            });            
    })
});