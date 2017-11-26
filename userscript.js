// ==UserScript==
// @name          3+3 game bot
// @namespace     http://github.com/neoatlantis/saechsli
// @description	  Experimental study of automated 3+3 gaming.
//
// @require https://code.jquery.com/jquery-2.1.4.min.js
// @include       https://d29zfk7accxxr5.cloudfront.net/games/game-156/data/*
// @grant         unsafeWindow
// ==/UserScript==

(function(){
//////////////////////////////////////////////////////////////////////////////

function moveGrid(direction){
    console.log("try trigger a keypress...");
    var dict = {
        "left": "left", "right": "right", "top": "up", "bottom": "down"};
    if(!direction || !dict[direction]) return;
    var button = unsafeWindow.game.controller.buttons[dict[direction]];
    button.trigger("keydown");
}

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
        dataType: "json",
    })
    .done(function(data){
        if(state.grid != data.hash) return;
        console.log(data.result);
        lastStateHash = state.grid; // mark as done
        moveGrid(data.choice);
    })
    .always(function(){
        setTimeout(askAdvice, 500);
    });
}

askAdvice();

//////////////////////////////////////////////////////////////////////////////
})();
