# wafflesolver
solver for the https://wafflegame.net/ word game to find the solution for an unsolved waffle and the shortest path towards the solution

out to James Robinson for creating this fun game!
https://x.com/jamesjessian

Play the game and maybe support James!
https://wafflegame.net/


Steps:
- wordlist preprocessing to find candidate words to speed up the next step
- bruteforce the solution with recursion
- when the solution is found find the shortest path to the solution using a combination of cycle decomposition and weighted BFS

the interesting files to look at are wafflesolver.py and cycle_decomposition.py

out to https://github.com/hellpig for their well-documented code for the same problem. it convinced me that cycle decomposition might be the best approach.

read this if you love strings and mutating them: https://epubs.siam.org/doi/abs/10.1137/080712969?journalCode=smjcat


to start just run either wafflesolver.py to bruteforce some sample waffles from wafflestate.py,

or run cycle_decomposition to solve all waffles as of 2024-11-07 from wafflegame.com in a few seconds



initially i tried to solve it using AStar, but Astar is mostly useless as there is no "right" estimate to the ideal solution that can be derived from just the current board state

the AStar code is still in there, run wafflesolver_old.py to see it in (in)action. takes up to a minute for some waffles because without good estimation it basically degrades into a dumb BFS.

that was a really fun problem to solve!
if you enjoy sorting things and pointless optimization and actually read this lmk!
@knmx___


