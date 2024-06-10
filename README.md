# CS50 Introduction to AI with Python - WIP

This repository contains my projects and assignments for the CS50: Introduction to AI with Python course.

## Table of Contents
- [Description](#description)
- [Installation and Usage](#installation-and-usage)
- [Projects](#projects)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Description

This repository includes all the code and projects I completed as part of the CS50: Introduction to AI with Python course.
The course covered various AI concepts, including search algorithms, logic, machine learning, and more.

## Installation and Usage - wip

To run the projects locally, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/DerickRedDanger/CS50AI.git
    cd CS50AI
    ```

2. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the projects:
    ```bash
    python project_name.py
    ```

## Projects

### **Search Algorithms** - Project 0

Projects focused on using search Algorithms to find the optimal path for a problem, like a navigator app that finds the best route from your origin to the destination, or like playing a game and figuring out the next move. This study included approaches like Depth-first search, breadth-first search, A* search, Greedy Best-First Search and Adversarial Search (Minimax, Alpha-Beta Pruning and Depth-Limited Minimax). For the projects, the methods utilized were breadth-first search and Adversarial Search (Minimax and Alpha-Beta Pruning). 

#### Project 0 - Degrees

This project follow the idea of the Six Degrees of Kevin Bacon game, where anyone in the Hollywood film industry can be connected to Kevin Bacon within six steps, where each step consists of finding a film that both actors starred in.

This project applies a breadth-first search to find the shortest path between any two actors by choosing a sequence of movies that connects them.For example, the shortest path between Jennifer Lawrence and Tom Hanks is 2: Jennifer Lawrence is connected to Kevin Bacon by both starring in “X-Men: First Class,” and Kevin Bacon is connected to Tom Hanks by both starring in “Apollo 13.”

#### Project 0 - Tic Tac Toe

This project aimed at creating a rule based Ai (weak Ai) that always makes optimal moves in a Tic Toc Toe game. This was done using Adversarial search Minimax with Alpha-Beta Pruning, So the Ai would simulate all possible moviments in a game until it's over, then, based on the result, it would backtrack, finding which move each player would do that would lead to their desired result (minimizing or maximizing the score, depending of the player).

As such, meanwhile it's possible to reach a draw against the Ai (since both sides playing optimally leads to a draw), you shouldn't be able to beat it.

### **Knowledge** - Project 1

Projects focused on creating Ai capable of knowledge engineering (that is representing knowledge and drawing conclusions)

search Algorithms to find the optimal path for a problem, like a navigator app that finds the best route from your origin to the destination, or like playing a game and figuring out the next move. This study included approaches like Depth-first search, breadth-first search, A* search, Greedy Best-First Search and Adversarial Search (Minimax, Alpha-Beta Pruning and Depth-Limited Minimax)



2. 
    - A project on logic-based AI and knowledge representation.
3. **Uncertainty**
    - Projects on probabilistic models and inference.
3. **Optimization**
    - Projects on probabilistic models and inference.
4. **Learning**
    - Machine learning projects, including classifiers and neural networks.
5. **Neural Networks**
    - Machine learning projects, including classifiers and neural networks.
6. **Language**
    - 

## Contributing

If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [CS50 Introduction to AI with Python](https://cs50.harvard.edu/ai/)
- The course instructors and teaching assistants.
