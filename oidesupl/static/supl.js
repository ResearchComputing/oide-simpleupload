'use strict';

angular.module('oide.supl', ['angularFileUpload','treeControl'])

.config(['$stateProvider','$urlRouterProvider',function($stateProvider,$urlRouterProvider) {
  $stateProvider
    .state('supl', {
      url: '/supl',
      templateUrl: '/static/supl/supl.html',
      controller: 'SuplCtrl'
    });
}])
.controller('SuplCtrl', ['$scope', 'FileUploader', '$modal','$log', function($scope,FileUploader,$modal,$log) {
  var uploader = $scope.uploader = new FileUploader({
       url: '/supl/a/upload',
       headers: {
                  'X-XSRFToken': getCookie('_xsrf')
                }
   });

  uploader.filters.push({
    name: 'customFilter',
    fn: function(item /*{File|FileLikeObject}*/, options) {
      return this.queue.length < 10;
    }
  });

   uploader.onWhenAddingFileFailed = function(item /*{File|FileLikeObject}*/, filter, options) {
       console.info('onWhenAddingFileFailed', item, filter, options);
   };
    uploader.onAfterAddingFile = function(fileItem) {
      fileItem.headers['uploadDir'] = $scope.dirpath;
      console.info('onAfterAddingFile', fileItem);
    };
   uploader.onAfterAddingAll = function(addedFileItems) {
       console.info('onAfterAddingAll', addedFileItems);
   };
   uploader.onBeforeUploadItem = function(item) {
       console.info('onBeforeUploadItem', item);
   };
   uploader.onProgressItem = function(fileItem, progress) {
       console.info('onProgressItem', fileItem, progress);
   };
   uploader.onProgressAll = function(progress) {
       console.info('onProgressAll', progress);
   };
   uploader.onSuccessItem = function(fileItem, response, status, headers) {
       console.info('onSuccessItem', fileItem, response, status, headers);
   };
   uploader.onErrorItem = function(fileItem, response, status, headers) {
       console.info('onErrorItem', fileItem, response, status, headers);
   };
   uploader.onCancelItem = function(fileItem, response, status, headers) {
       console.info('onCancelItem', fileItem, response, status, headers);
   };
   uploader.onCompleteItem = function(fileItem, response, status, headers) {
       console.info('onCompleteItem', fileItem, response, status, headers);
   };
   uploader.onCompleteAll = function() {
       console.info('onCompleteAll');
   };
   console.info('uploader', uploader);

   $scope.dirpath = 'No directory selected';

   $scope.selectDirectory = function (size) {

    var modalInstance = $modal.open({
      backdrop: 'static',
      keyboard: false,
      templateUrl: '/static/supl/dir-select-modal.html',
      controller: 'DirSelectModalCtrl',
      size: 'lg'
    });

    modalInstance.result.then(function (uploadDir) {
      if (uploadDir.hasOwnProperty('dirpath')) {
        $scope.dirpath = uploadDir.dirpath;
        if (!$scope.dirSelected) {
          $scope.dirSelected = true;
        }
      }
    }, function () {
      $log.info('Modal dismissed at: ' + new Date());
    });
  };
}])
.controller('DirSelectModalCtrl', function ($scope, $modalInstance, $http) {
  $scope.uploadDir = {};
  $scope.invalidFilepath = true;
  $scope.treeData = {};
  $scope.treeOptions = {
    multiSelection: false,
    isLeaf: function(node) {
      return node.type !== 'dir';
    },
    injectClasses: {
      iExpanded: "filetree-icon fa fa-folder-open",
      iCollapsed: "filetree-icon fa fa-folder",
      iLeaf: "filetree-icon fa fa-file",
    }
  };
  var initialContents = $http
    .get('/filebrowser/filetree/a/dir')
    .success(function(data, status, headers, config) {
      for (var i=0;i<data.length;i++) {
        data[i].children = [];
      }
      $scope.treeData.filetreeContents = data;
    }).
    error(function(data, status, headers, config) {
      $log.error('Failed to initialize filetree.');
    });
    $scope.getDirContents = function (node,expanded) {
      $http
        .get('/filebrowser/filetree/a/dir', {
          params: {
            dirpath: node.filepath
          }
        }).
        success(function(data, status, headers, config) {
          for (var i=0;i<data.length;i++) {
            if (!data[i].hasOwnProperty('children')) {
              data[i].children = [];
            }
          }
          node.children = data;
        }).
        error(function(data, status, headers, config) {
          $log.error('Failed to grab dir contents from ',node.filepath);
        });
  };

  $scope.updateDirName = function (node, selected) {
    $scope.invalidFilepath = false;
    if (node.type === 'dir') {
      $scope.uploadDir.dirpath = node.filepath;
    } else {
      var index = node.filepath.lastIndexOf('/')+1;
      var dirpath = node.filepath.substring(0,index);
      $scope.uploadDir.dirpath = dirpath;
    }
  };

  $scope.selectDir = function () {
    $modalInstance.close($scope.uploadDir);
  };

  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };
});
