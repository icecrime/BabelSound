"use strict";

function BabelSoundCtrl($scope, $http) {

    $scope.isLoading = function() {
       return $http.pendingRequests.length !== 0;
    };

    $scope.requestTranslation = function() {

        $scope.results = null;
        $scope.error_msg = null;

        $http.post('1/translate.json', {uri: $scope.trackURL}).
            success(function(data) {
                $scope.results = data.services;
            }).
            error(function(data) {
                $scope.error_msg = data.error_msg;
            });
    };

}
