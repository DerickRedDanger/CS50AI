Lecture 0: Search
Course Overview
Lecture 0 of the CS50 Introduction to AI with Python course focused on search algorithms, explaining their uses and implementations. Examples included navigation applications and game-playing strategies, such as Tic-Tac-Toe and chess. The lecture covered several search techniques:

Search Algorithms
Depth-First Search (DFS):

Explores a path to its end before backtracking. It can be fast if the solution is found early but may not find the optimal solution and can be time-consuming.
Breadth-First Search (BFS):

Explores all possible paths level by level, ensuring the shortest path is found. It guarantees the optimal solution but can be slow.
Greedy Best-First Search:

Uses a heuristic to expand the node closest to the goal. Faster than uninformed searches but may lead to suboptimal paths if the heuristic is inaccurate.
A Search:*

Combines the cost to reach the current node and the estimated cost to the goal for more accurate pathfinding. It relies on the heuristic's accuracy.
Adversarial Search:

Used in games, where AI competes against an opponent. Techniques include Minimax, Alpha-Beta Pruning, and Depth-Limited Minimax.
Minimax:

Simulates all possible game states to determine the best move. Provides an optimal strategy in zero-sum games but is computationally intensive.
Alpha-Beta Pruning:

Optimizes Minimax by ignoring branches that won’t affect the final decision, reducing the number of nodes evaluated.
Depth-Limited Minimax:

Limits the depth of the search to a predefined level, using an evaluation function to estimate utility from a given state. More manageable computational requirements but relies on the evaluation function's accuracy.
Projects
Degrees of Separation
Objective: Find the shortest path between two actors using the Six Degrees of Kevin Bacon concept.
Algorithm: Breadth-First Search (BFS)
Description: This project applies BFS to determine the shortest path of co-starring films connecting two actors. For example, Jennifer Lawrence to Tom Hanks involves "X-Men: First Class" and "Apollo 13."
Tic-Tac-Toe AI
Objective: Develop an AI that plays Tic-Tac-Toe optimally.
Algorithm: Minimax with Alpha-Beta Pruning
Description: The AI uses Minimax with Alpha-Beta Pruning to simulate all possible game moves, ensuring optimal play. It evaluates potential moves to maximize its score while minimizing the opponent's, guaranteeing a win or a draw.
What I Learned
Gained a deep understanding of various search algorithms and their applications.
Applied BFS to solve real-world problems like finding the shortest path between actors.
Developed an AI for Tic-Tac-Toe using Minimax and Alpha-Beta Pruning.
Learned optimization techniques to improve algorithm efficiency.
