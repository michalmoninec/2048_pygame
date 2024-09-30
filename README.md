# 2048_pygame

Simple implementation of 2048 game.
Two modes available: singleplayer and MCTS simulation.

## Status

-   Needs massive optimization, missing concurrency for mcts simulation, type annotations, ...

## Game

-   Singleplayer movement with arrows.
-   When two cells with same number collide, they combine.
-   Target is to hit value 2048 in single cell.
-   MCTS uses simulation of random movements till the game is over for every move based on best score for each direction.
