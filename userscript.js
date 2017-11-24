// ==UserScript==
// @name          3+3 game bot
// @namespace     http://github.com/neoatlantis/game-3plus3-advisor
// @description	  Experimental study of automated 3+3 gaming.
//
// @require https://code.jquery.com/jquery-2.1.4.min.js
// @include       https://d29zfk7accxxr5.cloudfront.net/games/game-156/data/*
// @grant         unsafeWindow
// ==/UserScript==

(function(){
//////////////////////////////////////////////////////////////////////////////

function getGameStatus(){
    var orig = unsafeWindow.game.grid;
    if(orig[0] === undefined) return null; // no valid input, game not begun?

    return {
        grid: orig.toString(),
        food: unsafeWindow.game.food,
    };
}

var lastStateHash = "";
var askAdvice = function(){
    var state = getGameStatus();
    if(!state || state.grid == lastStateHash){
        setTimeout(askAdvice, 500);
        return;
    };

    // send request
    $.ajax({
        url: "http://127.0.0.1:13333/" + state.grid + "/" + state.food + "/",
    })
    .done(function(data){
        lastStateHash = state.grid; // mark as done
        console.log(data);
    })
    .always(function(){
        setTimeout(askAdvice, 500);
    });
}

askAdvice();

//////////////////////////////////////////////////////////////////////////////
})();
