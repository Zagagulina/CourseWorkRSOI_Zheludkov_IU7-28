var app = angular.module('BibliographyChecker', [])
.config(function($interpolateProvider) {
        $interpolateProvider.startSymbol('//').endSymbol('//');
    });