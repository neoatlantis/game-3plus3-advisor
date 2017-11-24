// ==UserScript==
// @name          3+3 game bot
// @namespace     http://github.com/neoatlantis/game-3plus3-advisor
// @description	  Experimental study of automated 3+3 gaming.
// @include       https://d29zfk7accxxr5.cloudfront.net/games/game-156/data/*
// @grant         unsafeWindow
// ==/UserScript==

(function(){
//////////////////////////////////////////////////////////////////////////////

setInterval(function(){
    console.log(unsafeWindow.game.grid);
}, 3000);



//////////////////////////////////////////////////////////////////////////////
})();
