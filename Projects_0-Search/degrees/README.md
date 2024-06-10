# Read me

The problem and it's full description is avaliable in the link:
https://cs50.harvard.edu/ai/2024/projects/0/degrees/


## Introduction:

This project follow the idea of the Six Degrees of Kevin Bacon game, where anyone in the Hollywood film industry can be connected to Kevin Bacon within six steps, where each step consists of finding a film that both actors starred in.

We are interested in finding the shortest path between any two actors by choosing a sequence of movies that connects them. For example, the shortest path between Jennifer Lawrence and Tom Hanks is 2: Jennifer Lawrence is connected to Kevin Bacon by both starring in “X-Men: First Class,” and Kevin Bacon is connected to Tom Hanks by both starring in “Apollo 13.”

We can frame this as a search problem: our states are people. Our actions are movies, which take us from one actor to another (it’s true that a movie could take us to multiple different actors, but that’s okay for this problem). Our initial state and goal state are defined by the two people we’re trying to connect. By using breadth-first search, we can find the shortest path from one actor to another.

## Utilization:

* cd inside the degree folder

* Run in the terminal: Python degrees.py - to execute the program while using the large directory. (Given it's size, it may take a moment to fully load the large directory, use Python degrees.py small to load the small one)

* The terminal will prompt the user to give the name of the source actor. If there is more than one actor with the same name, you will be shown their information and prompted to give the ID of the desired one.

* Then you will be prompted to give the name of the target actor.

* If the source and the target are the same, the terminal will return 0 degrees of separation.

* If the source and the target are connected, the terminal will show the degrees of separation (up to 6 degree as per Six Degrees of Kevin Bacon game) and the path from the source to the target will show below it. If there are multiple shortest paths, any of them can be returned.

* If the source and the target are not connected, the terminal will show Not Connected. Warning: Considering the sheer amount of information in the CSV files, it could take minutes for the program to look up to 6 degrees until it returns not connected. (tested with both of the actors named Kevin Bacon in the Large.people.csv, taking from 2 to 6 minutes)

## Understanding:

This project is composed of 4 main parts. degrees.py, the main program of this project and where the logic to find the shortest part is. 

util.py is a utility file containing implementations of Node, StackFrontier and QueueFrontier.

The folders large and small each contain three csv files; Movies, people and stars, varying only in size. 

movies.csv contains the Id, title and year of the movies. 

people.csv contain the id, name and birth of the actors. 

stars.csv contains the id of the actions and the id of the movies they starred. 

The small foulder was used for debugging. While the large was the one used for testing.

Cs50 had already implemented the part responsible for running the code, loading and reading data from the Csv files. It was my duty to implement the shortest_path function, the part responsible for searching the shortest path between two actors.

I am not allowed to change any part of degrees.py beside the function shortest_path, but I am allowed to create new functions, import libraries and modify utils.py

Apart from shortest_path, I only modified util.node.

## Specification:

shortest_path should take as arguments the source actor and the target actor, then search throught the the three Csv files for the shortest path between both. 

If a path exist, it should return a list, where each list iten contains (movie_id, actor_id). If the source is also the target, it should return a empty list. If a path doesn't exist, it should return None.







