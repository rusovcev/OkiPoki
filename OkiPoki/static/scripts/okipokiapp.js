angular.module("okipoki", [/*'angular.filter',*/ /*'ui.bootstrap'*/ /*'ngRoute'*/])
    .run(function ($rootScope) {
        $rootScope.title = "OkiPoki game";
    })
    //.config(function ($locationProvider, $routeProvider) {
    //    //$locationProvider.html5Mode({ enabled: true, requireBase: true });
    //    $routeProvider
    //    .when("/login", { templateUrl: "templates/login.html", controller: "" })
    //    .when("/signup", { templateUrl: "signup.html", controller: "" })
    //    .otherwise({ redirectTo: "/" });
    //})
    .factory("getJsonFile", function ($http) {
        var getData = function (jsonFile) {
            return $http.get(jsonFile).then(function (response) { return response.data; });
        }
        return { getData: getData };
    })
    .directive('fileModel', ['$parse', function ($parse) {
        return {
            restrict: 'A',
            link: function (scope, element, attrs) {
                var model = $parse(attrs.fileModel);
                var modelSetter = model.assign;

                element.bind('change', function () {
                    scope.$apply(function () {
                        modelSetter(scope, element[0].files[0]);
                    });
                });
            }
        };

    }])
    .directive('myCurrentTime', ['$interval', 'dateFilter', function ($interval, dateFilter) {
          // return the directive link function. (compile function not needed)
          return function (scope, element, attrs) {
              var format,  // date format
                  stopTime; // so that we can cancel the time updates

              // used to update the UI
              function updateTime() {
                  element.text(dateFilter(new Date(), format));
              }

              // watch the expression, and update the UI on change.
              scope.$watch(attrs.myCurrentTime, function (value) {
                  format = value;
                  updateTime();
              });

              stopTime = $interval(updateTime, 1000);

              // listen on DOM destroy (removal) event, and cancel the next UI update
              // to prevent updating time after the DOM element was removed.
              element.on('$destroy', function () {
                  $interval.cancel(stopTime);
              });
          }
      }])
    .controller("standingsCtrl", function ($scope, $http, /*$modal,*/ $timeout) {
        $scope.standings = [];
        $scope.getStandings = function () {
            $http
                .get("/standings").then(
                function (flask) {
                    $scope.standings = flask.data.response;
                },
                function () {
                    console.log("ERROR(standings)?");
                }
                );
        }
        $scope.getStandings();
    })
    .controller("loggedplayersCtrl", function ($scope, $rootScope, $http, $interval, $location) {
        var stopTime;
        $scope.loggedPlayers = [];

        function getLoggedPlayers() {
            $http
                .get("/logged/players").then(
                function (flask) {
                    $scope.loggedPlayers = flask.data.response;
                    console.log(flask.data.response);
                },
                function () {
                    console.log("ERROR(logged)?");
                });
        }

        stopTime = $interval(getLoggedPlayers, 5000);

        $scope.invite = function (p) {
            $http.post("/invitation", { "message" : "invite", "who": p.name })
            .then(
                function (flask) { console.log('Flask respond to POST:', flask.data.response); },
                function () { console.log('error? Flask didnt respond?'); }
            );
        }

        $scope.accept = function (p) {
            $http.post("/invitation", { "message" : "accepted", "from" : p.name })
            .then(
                function (flask) {
                    console.log('Flask respond to POST:', flask.data.response);
                    window.location.href = "/board?gameID=" + flask.data.response.game.gameID + "&playerX=" + flask.data.response.game.playerX + "&playerO=" + flask.data.response.game.playerO + "&move=wait&Iam=X";
                },
                function () { console.log('error? Flask didnt respond?'); }
            );
        }

        $scope.go2play = function (p) {
            $http.get("/invitation", { params: { "player": p.name, "gameID" : p.gameID } }).then(
                function (flask) {
                    console.log("Flask respond to GET: ", flask.data.response);
                    window.location.href = "/board?gameID=" + p.gameID + "&playerX=" + flask.data.response.game.playerX + "&playerO=" + flask.data.response.game.playerO + "&move=wait&Iam=O";
                },
                function () {
                    console.log("ERROR()?");
                });

        }

        $scope.$on('$destroy', function () {
            // Make sure that the interval is destroyed too
            $inteval.cancel(stopTime);
        });
    })
    .controller("gameCtrl", function ($scope, $http, $interval, $location, $rootScope) {
        var params = location.search.substr(1).split('&');
        $scope.playerX = params[1].split('=')[1];
        $scope.playerO = params[2].split('=')[1];
        $scope.gameID = params[0].split('=')[1];
        $scope.move = params[3].split('=')[1];
        $scope.Iam = params[4].split('=')[1];
        $scope.call4rematch = false;
        console.log("--------URL params:---------");
        console.log("gameID: ", $scope.gameID);
        console.log("pl.X:   ", $scope.playerX);
        console.log("pl.O:   ", $scope.playerO);
        console.log("move:   ", $scope.move);
        console.log("I am:   ", $scope.Iam);
        console.log("----------------------------");
        $rootScope.title = $scope.playerX + " vs " + $scope.playerO;

        $scope.format = 'HH:mm:ss';
        $scope.gameover = false;

        $scope.board = [null, null, null, null, null, null, null, null, null];

        var stop;
        $scope.getGame = function () {
            // Don't start a new fight if we are already fighting
            if (angular.isDefined(stop)) return;

            stop = $interval( function () {
                if (!$scope.gameover) {
                    // get board from Flask
                    var response = $http
                        .get("/play", { params: { "gameID": $scope.gameID, "Iam" : $scope.Iam } })
                        .then(
                        function (flask) {
                            console.log("response from FLASK:", flask.data);
                            $scope.board = flask.data.response.board;
                            $scope.gameover = flask.data.response.gameOver;
                            if (flask.data.response.gameOver) {
                                if (flask.data.response.Won) {
                                    $rootScope.title = "You WON!";
                                    $rootScope.subtitle = "Congratulation!";
                                }
                                else {
                                    if (flask.data.response.Draw) {
                                        $rootScope.title = "Draw!";
                                        $rootScope.subtitle = "Well done.";
                                        if ($scope.playerX == "AI" || $scope.playerO == "AI")
                                            $scope.call4rematch = true;
                                    }
                                    else {
                                        $rootScope.title = "you lose...";
                                        $rootScope.subtitle = "don't give up!";
                                        if ($scope.playerX == "AI" || $scope.playerO == "AI")
                                            $scope.call4rematch = true;
                                    }
                                }
                            }
                            else {
                                if (flask.data.response.toplay == $scope.Iam) {
                                    $scope.pauseGame();
                                    activeFields();
                                    $rootScope.subtitle = "your move, " + $scope.Iam;
                                }
                                else {

                                }

                            }
                        },
                        function () { console.log("ERROR (GET): didn't get anything from FLASK?!"); });
                }
                else if (false) {

                }
                else {
                    $scope.pauseGame();
                }
            },
            5000);
        };

        $scope.ask4rematch = function () {
            $http.post("/invitation", { "message": "rematch", "gameID": $scope.gameID })
            .then(
                function (flask) {
                    console.log('Flask respond to POST:', flask.data.response);
                    $scope.gameID = flask.data.response.game.gameID;
                    $scope.playerX = flask.data.response.game.playerX;
                    $scope.playerO = flask.data.response.game.playerO;
                    $scope.move = "wait";
                    if ($scope.Iam == "X") $scope.Iam = "O";
                    else $scope.Iam = "X";
                    $scope.gameover = false;
                    stop = undefined;
                    $rootScope.title = $scope.playerX + " vs " + $scope.playerO;
                    $scope.getGame();
                    $scope.call4rematch = false;
                },
                function () { console.log('error? Flask didnt respond?'); }
            );
        }

        $scope.movePlayed = function (f) {
            $http.post("/play", { "gameID" : $scope.gameID, "Iam" : $scope.Iam, "move": f }).then(
                function (flask) {
                    $rootScope.subtitle = "wait for opponent's move...";
                    console.log('Flask respond to POST:', flask.data);
                    $scope.board = flask.data.response.board;
                    //$scope.gameover = flask.data.response.gameOver;
                    //if (flask.data.response.gameOver) {
                    //    if (flask.data.response.Won) {
                    //        $rootScope.title = "You WON!";
                    //        $rootScope.subtitle = "Congratulation!";
                    //    }
                    //    else {
                    //        if (flask.data.response.Draw) {
                    //            $rootScope.title = "Draw!";
                    //            $rootScope.subtitle = "Well done.";
                    //        }
                    //        else {
                    //            $rootScope.title = "you lose...";
                    //            $rootScope.subtitle = "don't give up!";
                    //        }
                    //    }
                    //}
                    //else {
                        stop = undefined;
                        $scope.getGame();
                    //}
                },
                function () {
                    console.log('error? Flask didnt respond?');
                }
            );
            //$scope.gameover = false;
            //stop = undefined;
        }

        $scope.pauseGame = function () {
            if (angular.isDefined(stop)) {
                $interval.cancel(stop);
                stop = undefined;
            }
        };

        var activeFields = function () {
            for (var i = 0; i < $scope.board.length; i++)
                if ($scope.board[i] == null)
                    $scope.board[i] = '';
        };

        if ($scope.move == "play") {
            $rootScope.subtitle = "your move, " + $scope.Iam;
            activeFields();
        }
        else {
            $rootScope.subtitle = "wait for opponent to...";
            stop = undefined;
            $scope.getGame();
        }

        $scope.$on('$destroy', function () {
            // Make sure that the interval is destroyed too
            $scope.stopGame();
        });
    })
    .controller("playerCtrl", function ($scope, $rootScope, $http, $filter, $modal, getJsonFile) {
    })
;
