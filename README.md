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

## Lectures and Projects

### **Search Algorithms** 

#### Lecture 0 Overview:
Lecture 0 focused on various search algorithms used in AI for solving problems such as pathfinding and game playing. The lecture covered both uninformed and informed search techniques, providing a solid foundation for understanding how AI can efficiently search for solutions.

#### Search Algorithms Covered

1. Depth-First Search (DFS):

Explores a path to its end before backtracking and exploring other paths. Can be faster if the solution is found early in the search path, but may not find the optimal solution and can be time-consuming if many paths need to be explored.

2. Breadth-First Search (BFS):

Explores all possible paths step by step, ensuring the shortest path is found. It guarantees finding the optimal solution, but can be slow, especially with many paths to explore.

3. Greedy Best-First Search:

Uses a heuristic to expand the node closest to the goal. Often faster than uninformed searches, but may lead to suboptimal paths if the heuristic is inaccurate.

4. A* Search:

Combines the cost to reach the current node and the estimated cost to the goal. More accurate in finding the optimal path compared to Greedy Best-First, but relies on the accuracy of the heuristic.


#### Adversarial Search:

Used in competitive environments like games, where AI competes against an opponent.

Techniques: Minimax, Alpha-Beta Pruning, Depth-Limited Minimax.

1. Minimax:

Simulates all possible game states to determine the best move. Provides optimal strategy in zero-sum games but is Computationally intensive.

2. Alpha-Beta Pruning:

Optimizes Minimax by ignoring branches that won’t affect the final decision, reducing the number of nodes evaluated but is still computationally intensive for large game trees.

3. Depth-Limited Minimax:

Limits the depth of the search to a predefined level, using an evaluation function. Is more manageable computational requirements but Relies on the accuracy of the evaluation function.

#### Project 0 Overview

1. Project A - Degrees of Separation:

Objective: Find the shortest path between two actors using the concept of the Six Degrees of Kevin Bacon.

Algorithm: Breadth-First Search (BFS)

Description: The project applies BFS to determine the shortest path of co-starring films connecting two actors. For example, the shortest path between Jennifer Lawrence and Tom Hanks involves two films: "X-Men: First Class" (connecting Jennifer Lawrence and Kevin Bacon) and "Apollo 13" (connecting Kevin Bacon and Tom Hanks).

2. Project B - Tic-Tac-Toe AI:

Objective: Develop an AI that plays Tic-Tac-Toe optimally, never losing a game.

Algorithm: Minimax with Alpha-Beta Pruning

Description: The AI uses Minimax with Alpha-Beta Pruning to simulate all possible game moves, ensuring optimal play. The AI evaluates potential moves to maximize its score while minimizing the opponent's, leading to an optimal strategy that guarantees a win or a draw.

#### What I Learned:

* Gained a deep understanding of various search algorithms and their applications in solving complex problems.
* Applied BFS to solve real-world problems like finding the shortest path between actors.
* Developed an AI for Tic-Tac-Toe using Minimax and Alpha-Beta Pruning, enhancing problem-solving and algorithmic thinking skills.
* Learned optimization techniques to improve algorithm efficiency, crucial for handling large datasets and complex problems.

### **Knowledge**

#### Lecture 1 Overview:

Lecture 1 of the CS50 Introduction to AI with Python course focused on how AI can represent and reason about knowledge. The lecture covered propositional logic and first-order logic, demonstrating how these systems can model real-world scenarios and draw conclusions.

#### Logic Systems:

#### Propositional Logic:

A system of logic where statements can be true or false.
* Propositional Symbols: Represent specific statements.
* Logical Connectives: AND, OR, NOT, implication (→), and biconditional (↔).
* Implication and Biconditional: Describe relationships between propositions.
* Model: A particular assignment of truth values to propositional symbols.
* Knowledge Base: A set of propositions known to be true.
* Entailment: A statement is entailed if it is true in every model where the knowledge base is true.
* Inference: Drawing new conclusions from the knowledge base.
* Inference Rules: Rules like Modus Ponens used to derive new propositions.
* Resolution: A rule of inference used for automated theorem proving.
* Knowledge Engineering: Designing a knowledge base and inference mechanisms.

#### First-Order Logic:

Extends propositional logic to include quantifiers and predicates.

* Universal Quantification (∀): Statements that apply to all members of a domain.
* Existential Quantification (∃): Statements that apply to at least one member of a domain.
* Allows for more expressive representations of knowledge.

#### Projects Overview:

1. Project A - Knights:

Objective: Determine who are knights (truth-tellers) and who are knaves (liars) based on their statements.

Logic System: Propositional Logic

Description: This project involves analyzing statements made by individuals to identify knights and knaves. Knights always tell the truth, while knaves always lie. The AI uses propositional logic to evaluate each statement and deduce the identity of each individual.

2. Project B -Minesweeper:

Objective: Develop an AI to play Minesweeper proficiently, using logic to identify safe spots and mines.

Logic System: Propositional Logic

Description: The AI gathers information from its moves and uses logical reasoning to deduce the location of mines. When no safe moves are evident, it makes educated guesses, balancing risk and reward. The AI was tested extensively, winning most games except when early guesses led to a mine or when the remaining moves involved high risk.

#### What I Learned:
* Gained a thorough understanding of propositional and first-order logic.
* Applied logical reasoning to solve complex puzzles and games.
* Learned how to represent knowledge in a structured way that allows for automated reasoning.
* Developed AIs for logical deduction and game playing, enhancing problem-solving and critical thinking skills.


### **Uncertainty**

#### Lecture 2 Overview:

Lecture 2 of the CS50 Introduction to AI with Python course focused on how to create AI that makes optimal decisions under conditions of uncertainty. The lecture covered key concepts in probability and statistical reasoning, providing a foundation for handling uncertain information.

#### Key Concepts:

* Probability: 

    * Possible Worlds: Different ways the world (situation) might be, each associated with a probability.
    * Axioms in Probability: Fundamental principles governing probability calculations.
    * Unconditional Probability: The likelihood of an event occurring without any given conditions.
    * Conditional Probability: The likelihood of an event occurring given that another event has occurred.
    * Random Variables: Variables whose values depend on the outcomes of a random phenomenon.
    * Independence: When the occurrence of one event does not affect the probability of another event.

* Bayes' Rule: A formula that describes how to update the probabilities of hypotheses when given evidence.

    * Joint Probability: The probability of two events happening together.
    * Probability Rules: Including negation, inclusion-exclusion, and marginalization, which help in computing probabilities.
    * Bayesian Networks: Graphical models that represent the probabilistic relationships among a set of variables.
    * Inference: The process of deducing new probabilities given a set of known probabilities.
    * Inference by Enumeration: Exhaustively considering all possible outcomes to compute probabilities.

* Sampling Methods:

    * Likelihood Weighting: A sampling method for approximate inference in Bayesian networks.

* Markov Models:

    * Markov Assumption: The future state depends only on the current state, not on the sequence of events that preceded it.
    * Markov Chain: A sequence of random variables where the Markov assumption holds.
    * Hidden Markov Models (HMMs): Models where the system being modeled is assumed to follow a Markov process with hidden states.
    * Sensor Markov Assumption: Observations depend only on the current state.

#### Projects Overview:

1. Project A - PageRank:

Objective: Create an algorithm similar to Google's PageRank to identify important or high-quality web pages.

Concepts Used: Probability, random variables, Markov models.

Description: The task involved implementing two approaches to rank pages in a corpus. The first approach used the random surfer model, simulating the behavior of a user randomly clicking links. The second approach used an iterative algorithm to converge on a ranking that reflects the importance of each page based on the structure of the web.

2. Project B - Heredity:

Objective: Develop an AI to assess the likelihood that a person will have a particular genetic trait.

Concepts Used: Bayesian networks, joint probability.

Description: This project involved calculating the probability of a person having certain genetic traits based on their parents' genes or, in the absence of this information, using unconditional probabilities. The AI used joint probability and Bayesian networks to model the genetic inheritance process and compute the likelihood of different genetic outcomes.

#### What I Learned:

* Gained a comprehensive understanding of probability theory and its applications in AI.
* Learned how to create AI that makes decisions under uncertainty using probabilistic reasoning.
* Developed skills in building and using Bayesian networks for probabilistic inference.
* Implemented algorithms for real-world applications like PageRank and genetic trait prediction, enhancing problem-solving and analytical skills.

### **Optimization**

#### Lecture 3 Overview:
Lecture 3 of the CS50 Introduction to AI with Python course focused on optimization, which involves choosing the best option among a set of possible solutions to a problem. The lecture covered various optimization techniques and their applications in AI.

#### Key Concepts:

* Local Search: An optimization technique that starts from a candidate solution and iteratively moves to a neighboring solution.

    * Hill Climbing: An algorithm that continuously moves towards the direction of increasing elevation/value to find the peak.
        * Variants:
            * Steepest-ascent Hill Climbing: Chooses the steepest uphill move.
            * Stochastic Hill Climbing: Randomly selects among uphill moves.
            * First-choice Hill Climbing: Randomly generates neighbors until one is better than the current.
            * Random-Restart Hill Climbing: Repeatedly runs hill climbing from random starting points.
    * Local Beam Search: Starts with multiple random solutions and explores their neighbors, keeping the best ones.
    * Simulated Annealing: Mimics the process of heating and slowly cooling to reach a minimum energy state, allowing occasional downhill moves to escape local maxima.
* Linear Programming: An optimization technique for a problem in which the objective function and constraints are linear.

* Constraint Satisfaction Problems (CSP): Problems where the solution must satisfy a number of constraints.

    * Node Consistency: Ensuring that all values in the variable’s domain satisfy the variable's unary constraints.
    * Arc Consistency: Ensuring that for every value of one variable, there is a consistent value in another variable.
    * Backtracking Search: A depth-first search algorithm for CSPs that incrementally builds candidates to the solutions and abandons a candidate as soon as it determines that the candidate cannot lead to a valid solution.
#### Project Overview:

1. Project - Crossword:

Objective: Develop an AI that generates a crossword puzzle based on given word and structure files.

Concepts Used: Constraint Satisfaction, Backtracking Search.

Description: This project involved creating an AI that generates a valid crossword puzzle by filling in words from a provided list (words.txt) into a specified structure (structure.txt). The AI uses constraint satisfaction techniques and backtracking search to ensure that the words fit correctly according to the constraints of the crossword structure.

#### What I Learned:

* Gained knowledge of various optimization methods and their applications in AI.
* Learned different approaches to local search, including hill climbing and simulated annealing.
* Developed skills in solving constraint satisfaction problems using techniques like node and arc consistency.
* Implemented an AI for generating crosswords, enhancing problem-solving and analytical skills in optimization.



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
