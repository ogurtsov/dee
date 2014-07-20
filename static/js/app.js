      var app = angular.module('App', ['ngResource', 'ui.ace'])
      app.config(function($interpolateProvider){
        $interpolateProvider.startSymbol('[[')
        $interpolateProvider.endSymbol(']]')
      })

      app.directive('onSave', function() {
        return function(scope, elm, attrs) {
          function applySave() {
            scope.$apply(attrs.onSave);
          };

          var isCtrl = false

          elm.bind('keyup', function(evt) {
            if(evt.which == 17) isCtrl = false
          })

          elm.bind('keydown', function(evt){
            if(evt.which == 17) isCtrl=true;
            if(evt.which == 83 && isCtrl == true) {
                applySave()
                evt.preventDefault()
                return false;
            }
          })

        }
      })

    app.directive('ngContextMenu', function ($parse) {
        var renderContextMenu = function ($scope, event, options) {
            if (!$) { var $ = angular.element; }
            $(event.target).addClass('context');
            var $contextMenu = $('<div>');
            $contextMenu.addClass('dropdown clearfix');
            var $ul = $('<ul>');
            $ul.addClass('dropdown-menu');
            $ul.attr({ 'role': 'menu' });
            $ul.css({
                display: 'block',
                position: 'absolute',
                left: event.pageX + 'px',
                top: event.pageY + 'px'
            });
            angular.forEach(options, function (item, i) {
                var $li = $('<li>');
                if (item === null) {
                    $li.addClass('divider');
                } else {
                    $a = $('<a>');
                    $a.attr({ tabindex: '-1', href: '#' });
                    $a.text(item[0]);
                    $li.append($a);
                    $li.on('click', function () {
                        $scope.$apply(function() {
                            item[1].call($scope, $scope);
                        });
                    });
                }
                $ul.append($li);
            });
            $contextMenu.append($ul);
            $contextMenu.css({
                width: '100%',
                height: '100%',
                position: 'absolute',
                top: 0,
                left: 0,
                zIndex: 9999
            });
            $(document).find('body').append($contextMenu);
            $contextMenu.on("click", function (e) {
                $(event.target).removeClass('context');
                $contextMenu.remove();
            }).on('contextmenu', function (event) {
                $(event.target).removeClass('context');
                event.preventDefault();
                $contextMenu.remove();
            });
        };
        return function ($scope, element, attrs) {
            element.on('contextmenu', function (event) {
                $scope.$apply(function () {
                    event.preventDefault();
                    var options = $scope.$eval(attrs.ngContextMenu);
                    if (options instanceof Array) {
                        renderContextMenu($scope, event, options);
                    } else {
                        throw '"' + attrs.ngContextMenu + '" not an array';                    
                    }
                });
            });
        };
    });

      function DashboardController($scope, $http, $resource){
        $scope.currentDir = location.hash.replace('#', '')
        $scope.messages = []
        $scope.opened_files = []
        $scope.file = null
        $scope.title = 'DEE: Environment Environment'
        $scope.current = {
          'directories': [],
          'files': []
        }

        var Directory = $resource('/api/directory/?dir=:dir')
        var File = $resource('/api/file/?path=:path')

        $scope.init = function(){
          if($scope.currentDir != ''){
            $scope.openDir()
          }
        }

        $scope.addMessage = function(type, text){
          $scope.messages.push({'type': type, 'text':text})
        }

        $scope.removeMessage = function(index){
          $scope.messages.splice(index, 1)
        }

        $scope.saveFile = function(){
            $scope.file.updated = false
            $scope.file.$save({}, function(data,headers){
                alert('success')
            }, function(data,headers){
                alert('failed')
            })
        }

        $scope.openFile = function(path){
          for(var index in $scope.opened_files){
            if($scope.opened_files[index].path == path){
              return
            }
          }
          
          File.get({'path': path})
            .$promise.then(function(file){
              $scope.opened_files.push(angular.copy(file))
              $scope.setFile()
            }, function(data){
              $scope.addMessage('danger', 'File doesn\'t exist of you don\'t have access to it')
            })
        }

        $scope.getAceMode = function(filename){
            var ext = filename.split('.')[filename.split('.').length - 1]
            var modes = {
                'py': 'python',
                'js': 'javascript',
                'rb': 'ruby',
                'html': 'html',
                'php': 'php'
              }
            return modes[ext]
        }

        $scope.aceLoaded = function(_editor) {
          _editor.setOptions({
            fontSize: "11pt"
          })
        }

        $scope.aceChanged = function(e) {
            $scope.file.updated = true
        }

        $scope.setFile = function(index){
          if(typeof index == 'undefined'){
            index = $scope.opened_files.length - 1
          }
          $scope.file = $scope.opened_files[index]
          //$scope.initEditor($scope.file.name)
        }

        $scope.closeFile = function(index){
            if(!confirm('All changes will be lost')){
                return false
            }
          if($scope.file.name == $scope.opened_files[index].name){
            if($scope.opened_files.length > 1 && index == 0){
              $scope.file = $scope.opened_files[1]
            }else if($scope.opened_files.length > 1 && index != 0){
              $scope.file = $scope.opened_files[index - 1]
            }
          }
          $scope.opened_files.splice(index, 1)
        }

        $scope.goBack = function(){
          if($scope.currentDir != '/'){
            var dir_chain = $scope.currentDir.split('/')
            dir_chain.splice(dir_chain.length - 2, 2)
            $scope.openDir(dir_chain.join('/'))
          }
        }

        $scope.openDir = function(_dir){
          $scope.currentDir = _dir || $scope.currentDir
          if($scope.currentDir[$scope.currentDir.length-1] != '/'){
            $scope.currentDir += '/'
          }
          location.hash = $scope.currentDir
          Directory.get({'dir': $scope.currentDir})
            .$promise.then(function(data){
                $scope.title = _dir
                $scope.current.directories = []
                $scope.current.files = []
                for(var index in data.children){
                  data.children[index].type === 'file'
                    ? $scope.current.files.push(data.children[index])
                    : $scope.current.directories.push(data.children[index])
                }
            }, function(data){
                $scope.addMessage('danger', 'Directory doesn\'t exist of you don\'t have access to it')
            })
        }
        
        $scope.dirOptions = [
            ['New File', function ($dirScope) {
                console.log('new file', $dirScope.d)
            }],
            null,
            ['New Folder', function ($dirScope) {
                console.log('new folder', $dirScope.d)
            }],
            null,
            ['Rename', function ($dirScope) {
                console.log('rename dir', $dirScope.d)
            }],
            null,
            ['Delete', function ($dirScope) {
                console.log('delete dir', $dirScope.d)
            }]
        ]
        
        $scope.fileOptions = [
            ['Rename', function ($fileScope) {
                console.log('rename file', $fileScope.f)
            }],
            null,
            ['Delete', function ($fileScope) {
                console.log('delete file', $fileScope.f)
            }]
        ]

      }
