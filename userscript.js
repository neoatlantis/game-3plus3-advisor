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

    var grid = [
        [orig[0], orig[1], orig[2], orig[3]],
        [orig[4], orig[5], orig[6], orig[7]],
        [orig[8], orig[9], orig[10], orig[11]],
        [orig[12], orig[13], orig[14], orig[15]],
    ], food = unsafeWindow.game.food;

    return {
        hash: orig.toString(),
        grid: grid,
        food: food,
    };
}

var lastStateHash = "";

var giveAdvice = function(){
    var state = getGameStatus();
    if(!state) return;
    if(state.hash == lastStateHash) return;

    // send request
    $.ajax({
        url: "http://127.0.0.1:13333/",
        dataType: "jsonp",
    })
    .always(function(){
        setTimeout(giveAdvice, 500);
    });
}

giveAdvice();

//////////////////////////////////////////////////////////////////////////////
})();
