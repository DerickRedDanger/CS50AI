# Degrees of Separation

The full problem description is available [CS50 AI Project 2: Degrees](https://cs50.harvard.edu/ai/2024/projects/0/degrees/).

## Introduction

This project is inspired by the Six Degrees of Kevin Bacon game, where any actor in Hollywood can be connected to Kevin Bacon within six steps. Each step involves finding a movie that both actors have starred in. 

Our objective is to find the shortest path between any two actors by choosing a sequence of movies that connects them. For example, the shortest path between Jennifer Lawrence and Tom Hanks is two steps:
1. Jennifer Lawrence starred with Kevin Bacon in “X-Men: First Class.”
2. Kevin Bacon starred with Tom Hanks in “Apollo 13.”

We frame this as a search problem:
- **States:** People (actors).
- **Actions:** Movies, which link actors.
- **Initial State and Goal State:** Defined by the two actors we are trying to connect.

Using breadth-first search (BFS), we find the shortest path from one actor to another.

## Usage

1. Navigate to the `degrees` folder.
   ```
   cd degrees
   ```
2. Run the program:
   ```
   python degrees.py
   ```
   To use the smaller dataset for faster execution, run:
   ```
   python degrees.py small
   ```
3. The terminal will prompt for the name of the source actor. If multiple actors share the name, their details and IDs will be displayed, prompting you to choose the correct one.
4. Enter the name of the target actor.
5. The program will then:
   - Show 0 degrees of separation if the source and target are the same.
   - Display the degrees of separation and the path if the source and target are connected (up to 6 degrees).
   - Indicate "Not Connected" if there is no path. (Note: Searching up to 6 degrees can take several minutes due to the data size.)

## Understanding the Code

### degrees.py

This is the main program containing the logic to find the shortest path between two actors. CS50 provided the code for running the program, loading, and reading data from the CSV files. The `shortest_path` function is implemented by me to search for the shortest path between two actors.

### util.py

This utility file contains implementations for:
- `Node`: Represents a node in the search tree.
- `StackFrontier`: Implements a stack for depth-first search (DFS).
- `QueueFrontier`: Implements a queue for breadth-first search (BFS).

### Data Files

The `large` and `small` folders each contain three CSV files:
- `movies.csv`: Contains the ID, title, and year of movies.
- `people.csv`: Contains the ID, name, and birth year of actors.
- `stars.csv`: Contains the IDs of actors and the movies they starred in.

The `small` folder is used for debugging, while the `large` folder is used for testing.

## Implementation Details

### shortest_path Function

This function takes two arguments: the source actor and the target actor. It searches through the three CSV files to find the shortest path between them. The function:
- Returns a list of tuples `(movie_id, actor_id)` if a path exists.
- Returns an empty list if the source and target are the same.
- Returns `None` if no path exists.

### Constraints

I am allowed to create new functions, import libraries, and modify `utils.py`. However, I cannot change any part of `degrees.py` besides the `shortest_path` function.

