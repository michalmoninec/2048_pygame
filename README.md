# 2048_pygame

Simple implementation of 2048 game.
Two modes available: singleplayer and MCTS simulation.

## Status

-   Needs massive optimization, error handling, performance optimization, docstrings.

## Game

-   Singleplayer movement with arrows.
-   When two cells with same number collide, they combine.
-   Target is to hit value 2048 in single cell.
-   MCTS uses simulation of random movements till the game is over for every move based on best score for each direction.

## TODO:

-   Performance balance.
-   Threading to control UI and run simulation so it wont freeze.
-   "game" module update and optimization + clean-up.
-   MCTS improvement.
