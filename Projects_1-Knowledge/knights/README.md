# Knights and Knaves Puzzle Solver

The full problem description is available [CS50 AI Project 2: Knights](https://cs50.harvard.edu/ai/2024/projects/1/knights/).

## Introduction
This project is based on the "Knights and Knaves" puzzles from the book "What is the Name of This Book?" by Raymond Smullyan (1978).

In a Knights and Knaves puzzle:
- Each character is either a knight or a knave.
- A knight always tells the truth.
- A knave always lies.

The objective is to determine, based on a set of statements made by the characters, whether each character is a knight or a knave.

In this project, the goal is to represent these puzzles using propositional logic so that an AI running a model-checking algorithm can solve them.

## Usage
1. Navigate to the `knights` folder.
2. Run the following command in the terminal:
   ```bash
   python puzzle.py
   ```
The terminal will display which characters in each puzzle are knights and which are knaves.

## Understanding the Code

### logic.py
This file, provided by CS50, contains classes for different types of logical connectives (And, Or, Not, Biconditional, Implication) and a `model_check` function. The `model_check` function takes a knowledge base and a query, recursively considers all possible models, and returns True if the knowledge base entails the query, and False otherwise.

### puzzle.py
This file contains four different knowledge bases (`knowledge0`, `knowledge1`, `knowledge2`, `knowledge3`) corresponding to the solutions for puzzles 0, 1, 2, and 3. These knowledge bases were initially empty, and my task was to populate them.

## Specifications
Each character in the following sentences is either a knight or a knave. Every sentence spoken by a knight is true, and every sentence spoken by a knave is false.

**Note:** Below, you will see all knowledge that could be inferred based on the statements made by the characters, even those that clearly can't be true. This is because the AI is responsible for the logical deductions.

### Puzzle 0:
A says, "I am both a knight and a knave."

**Knowledge 0:**
- One person can be a knight or a knave.
- But not both.
- If A is telling the truth, A is a knight.
- If A is lying, A is a knave.

### Puzzle 1:
A says, "We are both knaves."

B says nothing.

**Knowledge 1:**
- One person can be a knight or a knave.
- But not both.
- If A is telling the truth, A is a knight.
- If A is lying, A is a knave.

### Puzzle 2:
A says, "We are the same kind."

B says, "We are of different kinds."

**Knowledge 2:**
- One person can be a knight or a knave.
- But not both.
- A is a knight if they are both knights or both knaves.
- A is a knave if they are of different kinds.
- B is a knight if they are of different kinds.
- B is a knave if they are both knights or both knaves.

### Puzzle 3:
A says either "I am a knight." or "I am a knave." but you don't know which.

B says, "A said 'I am a knave'."

B says, "C is a knave."

C says, "A is a knight."

**Knowledge 3:**
- One person can be a knight or a knave.
- But not both.
- A is a knight if they are either a knight or a knave.
- A is a knave if they are neither a knight nor a knave.
- If B is a knight, then A indeed said that and B is a knave. In this case, A is a knight if B is a knave.
- If B is a knight, then A indeed said that and B is a knave. In this case, A is a knave if B is a knight.
- If B is a knave, then we can't imply anything as B could be lying.
- B is a knight if C is a knave.
- B is a knave if C is a knight.
- C is a knight if A is a knight.
- C is a knave if A is a knave.

```

Feel free to make any additional changes or let me know if there's anything else you'd like to include!