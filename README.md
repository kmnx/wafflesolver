# wafflesolver
solver for the https://wafflegame.net/ word game to find the solution for an unsolved waffle and the shortest path towards the solution

out to James Robinson for creating this fun game!
https://x.com/jamesjessian

Play the game and maybe support James!
https://wafflegame.net/


Steps:
- wordlist preprocessing to find candidate words to speed up the next step
- bruteforce the solution with recursion
- when the solution is found find the shortest path to the solution using a combination of cycle decomposition and weighted Breadth First Search

the interesting files to look at are wafflesolver.py and cycle_decomposition.py

out to https://github.com/hellpig for their well-documented code for the same problem. it convinced me that cycle decomposition might be the best approach.

read this if you love strings and mutating them: https://epubs.siam.org/doi/abs/10.1137/080712969?journalCode=smjcat


to start run either wafflesolver.py to bruteforce some sample waffles from wafflestate.py,

or run cycle_decomposition to find the shortest paths for all waffles as of 2024-11-07 from wafflegame.com



initially i tried to solve it using AStar. But AStar does not work for waffles as it requires an estimate of the distance to the goal based on the current board state, something which is impossible for this game.

the AStar code is still in there, run wafflesolver_oldest.py to see it in (in)action. takes up to a minute for some waffles because without good estimation it degrades into an unguided Breadth First Search.

the current approach with filtering, recursion and cycle decomposition takes about 0.5 milliseconds per gridsize 5 puzzle and about 15ms for size 7.
