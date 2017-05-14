angular.module('BibliographyChecker')
  .controller('moderatedController', function($scope, $http, $window) {
    $scope.waiting = true;
    $scope.waiting1 = true;
    $scope.waiting2 = true;
    $scope.PublishersListID = [];
    $scope.PublishersListModeratedID = [];
    
    $http.get("/publishersNotModerated")
        .then(function(response) {
            $scope.PublishersList = response.data['publishers'];
            $scope.selected = $scope.PublishersList[0];
            $scope.size = Math.min($scope.PublishersList.length, 7);
            $scope.waiting1 = false;
        },
        function(response) {
            $window.location.href = "/error?message=" +response.data['message'];
        });
        
    $http.get("/publishersModerated")
        .then(function(response) {
            $scope.PublishersListM = response.data['publishers'];
            $scope.sizeM = Math.min($scope.PublishersListM.length, 7);
            $scope.waiting2 = false;
        },
        function(response) {
            $window.location.href = "/error?message=" +response.data['message'];
        });      
   
    $scope.setWaitingFalse = function() {
        if (($scope.waiting1 == false) && ($scope.waiting2 == false))
        {
            $scope.waiting = false;
        }
    }
   
    $scope.$watch('waiting1', 
    function() {
        $scope.setWaitingFalse();
    },
    true)
    
    $scope.$watch('waiting2', 
    function() {
        $scope.setWaitingFalse();
    },
    true)
   
    $scope.$watch('selected', 
    function() {
        $scope.showT = false;
        $http.get("/templateInfoFull/" + $scope.selected.id)
            .then(function(response) {
                $scope.TemplateList = response.data['templateInfo']['templateList'];
                if ($scope.TemplateList.length != 0)
                {
                    $scope.selectedTemplate = $scope.TemplateList[0];
                    $scope.showT = true;
                }
                $scope.sizeT = Math.min($scope.TemplateList.length, 7);
            },
            function(response) {
                $scope.showT = false;
            });
    }, 
    true);
    
    $scope.moveToModerate = function() {
        var wasIndex = $scope.PublishersListID.indexOf($scope.selected.id);
        if (wasIndex != -1)
        {
            $scope.PublishersListID.splice(wasIndex, 1);
        }
        else
        {
            $scope.PublishersListModeratedID.push($scope.selected.id);
        }
        $scope.PublishersListM.push($scope.selected);
    }
    
    $scope.moveToNotModerate = function() {
        var wasIndex = $scope.PublishersListModeratedID.indexOf($scope.selected.id);
        if (wasIndex != -1)
        {
            $scope.PublishersListModeratedID.splice(wasIndex, 1);
        }
        else
        {
            $scope.PublishersListID.push($scope.selected.id);
        }
        $scope.PublishersList.push($scope.selected);
    }
    
    $scope.containInList = function(list)
    {
        var res = -1;
        for (var i = 0; i < list.length; i++) {
            if (list[i].id == $scope.selected.id)
            {
                res = i;
                break;
            }
        }        
        return res;
    }
    
    $scope.move = function() {
        var notMIndex = $scope.containInList($scope.PublishersList);
        if (notMIndex != -1)
        {
            $scope.PublishersList.splice(notMIndex, 1);
            $scope.moveToModerate();
        }
        else
        {
            var mIndex = $scope.containInList($scope.PublishersListM);
            $scope.PublishersListM.splice(mIndex, 1);
            $scope.moveToNotModerate();
        }
    }
    
    $scope.postData = function() {
        $scope.waiting = true;
        
        var data = {
                notModerated: $scope.PublishersListID,
                moderated: $scope.PublishersListModeratedID
            };        
        $http.post("/moderateSaveChange", data)
              .then(function(response) {
                  $scope.PublishersListID.length = 0;
                  $scope.PublishersListModeratedID.length = 0;
                  $scope.waiting = false;
              },
              function(response) {
                  $window.location.href = "/error?message=" +response.data['message'];
              })
    };
});