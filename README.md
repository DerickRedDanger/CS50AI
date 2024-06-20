# CS50 Introduction to AI with Python - WIP

This repository contains my projects and assignments for the CS50: Introduction to AI with Python course.

## Table of Contents
- [Description](#description)
- [Installation and Usage](#installation-and-usage)
- [Search Algorithms](#search-algorithms)
    - [Project 0](#project-0)
- [Knowledge](#knowledge)
    - [Project 1](#project-1)
- [Uncertainty](#uncertainty)
    - [Project 2](#project-2)
- [Optimization](#optimization)
    - [Project 3](#project-3)
- [Machine Learning](#machine-learning)
    - [Project 4](#project-4)
- [Neural Networks](#neural-networks)
    - [Project 5](#project-5)
- [Language](#language)
    - [Project 6](#project-6)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Description

This repository includes all the code and projects I completed as part of the CS50: Introduction to AI with Python course, including a summary of everything I learned during it.

## Installation and Usage

To run the projects locally, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/DerickRedDanger/CS50AI.git
    cd CS50AI
    ```

2. Navigate to the project directory you'd like to run. Each project has its own README explaining how to run it:
    ```bash
    cd Project_5-Neural_Networks
    ```

## Lectures and Projects

### Search Algorithms

#### Lecture 0
Lecture 0 focused on various search algorithms used in AI for solving problems such as pathfinding and game playing. The lecture covered both uninformed and informed search techniques, providing a solid foundation for understanding how AI can efficiently search for solutions.

#### Search Algorithms Covered
- **Depth-First Search (DFS):** Explores a path to its end before backtracking. Can be fast if the solution is early in the search path but may not find the optimal solution.
- **Breadth-First Search (BFS):** Explores all possible paths step by step, ensuring the shortest path is found. Guarantees finding the optimal solution but can be slow.
- **Greedy Best-First Search:** Uses a heuristic to expand the node closest to the goal. Often faster than uninformed searches but may lead to suboptimal paths.
- **A* Search:** Combines the cost to reach the current node and the estimated cost to the goal. More accurate in finding the optimal path but relies on the heuristic's accuracy.

#### Adversarial Search
- **Minimax:** Simulates all possible game states to determine the best move. Provides optimal strategy in zero-sum games but is computationally intensive.
- **Alpha-Beta Pruning:** Optimizes Minimax by ignoring branches that won’t affect the final decision, reducing the number of nodes evaluated.
- **Depth-Limited Minimax:** Limits the depth of the search to a predefined level, using an evaluation function.

#### Project 0
- **Project A - Degrees of Separation:** Finds the shortest path between two actors using BFS.
- **Project B - Tic-Tac-Toe AI:** Develops an AI that plays Tic-Tac-Toe optimally using Minimax with Alpha-Beta Pruning.

#### What I Learned
- Understanding of various search algorithms and their applications.
- Applied BFS to solve real-world problems like finding the shortest path between actors.
- Developed an AI for Tic-Tac-Toe using Minimax and Alpha-Beta Pruning.

### Knowledge

#### Lecture 1
Lecture 1 focused on how AI can represent and reason about knowledge using propositional and first-order logic.

#### Project 1
- **Project A - Knights:** Determines knights (truth-tellers) and knaves (liars) based on their statements using propositional logic.
- **Project B - Minesweeper:** Develops an AI to play Minesweeper proficiently using propositional logic.

#### What I Learned
- Understanding of propositional and first-order logic.
- Applied logical reasoning to solve complex puzzles and games.

### Uncertainty

#### Lecture 2
Lecture 2 focused on creating AI that makes optimal decisions under uncertainty using probability and statistical reasoning.

#### Project 2
- **Project A - PageRank:** Creates an algorithm similar to Google's PageRank to identify important web pages.
- **Project B - Heredity:** Develops an AI to assess the likelihood of genetic traits.

#### What I Learned
- Comprehensive understanding of probability theory and its applications in AI.
- Skills in building and using Bayesian networks for probabilistic inference.

### Optimization

#### Lecture 3
Lecture 3 focused on optimization techniques used in AI, including local search and constraint satisfaction problems.

#### Project 3
- **Project - Crossword:** Develops an AI that generates a crossword puzzle based on given word and structure files using constraint satisfaction techniques.

#### What I Learned
- Knowledge of various optimization methods and their applications.
- Solving constraint satisfaction problems using techniques like node and arc consistency.

### Machine Learning

#### Lecture 4
Lecture 4 focused on machine learning techniques and their applications in AI, including supervised and unsupervised learning.

#### Project 4
- **Project - Shopping:** Creates a classifier AI that predicts whether a user on a shopping website will purchase something.
- **Project - Nim:** Develops an AI capable of teaching itself to play Nim through reinforcement learning.

#### What I Learned
- Knowledge of various machine learning methods and their applications.
- Creating AI agents that learn through interaction and rewards.

### Neural Networks

#### Lecture 5
Lecture 5 focused on neural networks and their applications in AI, including designing and training neural networks.

#### Project 5
- **Project - Traffic:** Creates a neural network capable of classifying road signs based on images using TensorFlow's Keras.

#### What I Learned
- Designing and training neural networks.
- Advanced techniques like dropout to prevent overfitting and backpropagation for efficient training.

### Language

#### Lecture 6
Lecture 6 focused on natural language processing (NLP) and various applications such as automatic summarization and machine translation.

#### Project 6
- **Project - Language Modeling:** Develops an AI to perform text generation based on given input using NLP techniques.

#### What I Learned
- Understanding of NLP and its applications.
- Skills in building AI for text generation and other NLP tasks.

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue if you have any suggestions or improvements.

## License

This repository is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgments
I would like to thank the CS50 team for creating such an insightful and comprehensive course on AI. Special thanks to the instructors and course staff for their dedication and support.

