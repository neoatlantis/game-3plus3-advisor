Sächsli: an Automated Bot for Game 3+3
======================================

This is an automated bot for game [3+3][3P3]. Beside the link, the game is
available on the chat software Telegram by calling its @gamee bot.

_Saechsli_ plays this game automatically, and may achieve a score of
10000-20000(a matter of luck). It serves as a browser userscript, and
communicates a background service on Python, the latter doing searches and
instructs the former.

## Requirements

* `python3`, with packages:
    * `bottle`
* a browser(preferable Firefox or Chrome), with plugins:
    * `Greasemonkey` or `Tampermonkey`

## Usage

1. install the [userscript][US]
2. fire up the background service: `python3 __main__.py`
3. browse to the game via [URL][3P3], or open `web.telegram.org` and call
   a `@gamee` bot to do that.
4. begin the game. After blocks start showing up, _Saechsli_ shall take over
   the action.
5. Watch!

## Remarks

* This work is not intended to cheat(and why, experienced human player may do
  much better), but for study how to solve such a puzzle by using algorithms.
  Do not use it to trouble anyone.
* Currently Saechsli will search 4-6 steps basing on current grid status, and
  pick the best one with 1) the maximal reachable number in a cell, as well as
  2) the maximal freedom degrees after one movement. This differs in practice
  from a human solution. You are encouraged to write more criterions for that.




[3P3]: https://www.gameeapp.com/game/FGM7TVW2Ma 
[US]: https://github.com/neoatlantis/saechsli/blob/master/userscript.js
