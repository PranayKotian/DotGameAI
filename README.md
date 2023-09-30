# DotGameAI
Implementation of a genetic algorithm to solve a simple game where a dot must find its way to a goal. 

![DotGameGenerations](/readme_imgs/gens.jpg?raw=true "DotGameGenerations")

This fitness function optimizes for distance to the goal which would be extremely inefficient if there were any obstacles which required the dots to move away from the goal to eventually reach it (i.e. any type of maze). This game was created mostly to develop a general sense of how genetic algorithms work. 