var TodoControllers = angular.module('TimetableControllers', []);

TodoControllers.controller('TimetableCtrl', ['$scope', '$dragon', function ($scope, $dragon) {
    $scope.timetable = {};
    $scope.classInstances = [];
    $scope.channel = 'timetables';

    $dragon.onReady(function() {
        
        $dragon.subscribe('timetable', $scope.channel, {timetable__id: 1}).then(function(response) {
            $scope.dataMapper = new DataMapper(response.data);
        });

        $dragon.getSingle('timetable', {id:1}).then(function(response) {
            $scope.timetable = response.data;
        });

        $dragon.getList('classInstance', {timetable_id:1}).then(function(response) {
            $scope.classInstances = response.data;
        });
    });

    $dragon.onChannelMessage(function(channels, message) {
        if (indexOf.call(channels, $scope.channel) > -1) {
            $scope.$apply(function() {
                $scope.dataMapper.mapData($scope.todoItems, message);
            });
        }
    });

    $scope.addClass = function(classInstance) {
        col = classInstance.base.day;
        rowfrom = classInstance.base.timeFrom;
        rowTo = classInstance.base.timeTo;
        $dragon.update('todo-item', item);
    }
}]);
