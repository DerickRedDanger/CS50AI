# Crossword Project

## Problem Description
The full problem description is available at the following link:  [CS50 AI Project 3 - Crossword](https://cs50.harvard.edu/ai/2024/projects/3/crossword/)

## Introduction

This project aims to create an AI capable of generating a crossword puzzle, given a file representing the crossword's structure and a file containing all the words available for use.

The AI reads the structure file, recognizing the spaces for the words, their lengths, directions, and where they overlap with other words. For each variable, it creates a domain containing all words in the words file, then removes those that don't fit the variable's length.

Finally, it loops through each variable, trying the available words and backtracking if needed, until all words fit the constraints.

To optimize the process, it prioritizes the unassigned variable with the least number of remaining words, using the variable with the most overlaps as a tiebreaker. For each variable, it tries words in the order of the least constraining word, meaning the words that eliminate the fewest number of words from its overlapping variables when chosen.

The limitation for this crossword is that each word must be unique.

## Utilization

1. Navigate to the `crossword` directory:
   ```bash
   cd crossword
   ```
2. Run the following command in the terminal to generate a crossword:
   ```bash
   python generate.py data/structure.txt data/words.txt
   ```
   Here, `structure` and `words` can be `1`, `2`, or `3`. You can also create your own structure or word file.

3. If it's possible to create a crossword with the provided structure and words, the terminal will display the crossword representation. If not, it will return 'No Solution'.

4. To generate a PNG representing the crossword (you may need to run `pip3 install pillow` if you haven't already), add `output.png` at the end of the command:
   ```bash
   python generate.py data/structure1.txt data/words1.txt output.png
   ```

## Background

Generating a crossword puzzle involves choosing which words should go in each vertical or horizontal sequence of squares, given the structure of the crossword and a list of words. This problem can be modeled as a constraint satisfaction problem. Each sequence of squares is a variable, and we need to decide its value (which word from the domain will fill that sequence).

These variables have both unary and binary constraints. The unary constraint on a variable is given by its length. The binary constraints are given by its overlap with neighboring variables.

For each pair of neighboring variables, those variables share an overlap: a single square that is common to both. This overlap can be represented as the character index in each variable’s word that must be the same character.

An additional constraint is that all words must be unique: no word should be repeated multiple times in the puzzle.

The challenge was to write a program to find a satisfying assignment: a different word (from a given vocabulary list) for each variable such that all the unary and binary constraints are met.

## Understanding

This project consists of the files `crossword.py`, `generate.py`, and the directory `data`.

`crossword.py` was fully implemented by CS50 and contains the base of the crossword, including the `Crossword` class (representing the puzzle) and the `Variable` class (representing a variable in the crossword).

The `data` directory contains the words and structures used to make and test this project. You can create your own files as well. In a structure file, the '_' character represents a blank cell (a space for a letter), and any other character represents a cell that won't be filled. The words file defines a list of words (one per line) for the puzzle vocabulary.

`generate.py` contains the project's logic. CS50 defined the `CrosswordCreator` class to solve the crossword puzzle. It also includes the `print` function (responsible for showing the solution in the terminal), `save` (which can generate an image file of the solution), and `letter_grid` (a helper function used by both `print` and `save` to generate a 2D list of all characters in their appropriate positions for a given solution).

The `solve` function performs three tasks:
1. Calls `enforce_node_consistency` to ensure node consistency in the crossword puzzle, ensuring that every value in a variable’s domain satisfies the unary constraints.
2. Calls `ac3` to enforce arc consistency, ensuring that binary constraints are satisfied.
3. Calls `backtrack` on an initially empty assignment to try to find a solution to the problem.

My task was to complete the implementation of `enforce_node_consistency`, `revise`, `ac3`, `assignment_complete`, `consistent`, `order_domain_values`, `select_unassigned_variable`, and `backtrack` in `generate.py`. I also implemented the `queue_2s` and `get_arcs` functions to assist my functions.

## Specification

### `enforce_node_consistency`

- Updates `self.domains` such that each variable's domains are node consistent.
- Ensures that each value in a variable's domain has the same number of letters as the variable's length.

### `revise`

- Takes two variables (`X`, `Y`) as input and enforces arc consistency between them.
- Ensures `X` is arc consistent with `Y` when every value in the domain of `X` has a possible value in the domain of `Y` that does not cause a conflict (i.e., a square for which two variables disagree on the character value).
- Only modifies the domain of `X`.
- Returns `True` if an update was made to the domain of `X`; otherwise, returns `False`.

### `ac3`

- Enforces arc consistency across all arcs given as input.
- Takes arcs as input (list of tuples of two variables `(x,y)`) and enforces arc consistency on them. If no arcs are given, enforces arc consistency on all overlapping variables.
- Queues each arc, passes both to `revise`, and if `X` is updated, queues tuples of all other variables that overlap with `X`.
- Uses the `queue_2s` function to simulate a queue using two stacks.
- Returns `False` if during this process all values of a variable's domain are removed, indicating it's impossible to solve the problem.

### `assignment_complete`

- Takes an assignment dictionary as input, where each key is a variable object used in `CrosswordCreator` and the value is the word for that variable. Any unassigned variable won't be in this dictionary.
- Checks if a given assignment is complete (i.e., all variables are in the dictionary and have a value).
- Returns `True` if the assignment is complete; otherwise, returns `False`.

### `consistent`

- Checks if a given assignment is consistent.
- An assignment is consistent if it satisfies all problem constraints: all values are distinct, every value is the correct length, and there are no conflicts between neighboring variables.
- Returns `True` if the assignment is consistent; otherwise, returns `False`.

### `order_domain_values`

- Takes a variable `var` and current assignments as input.
- Returns a list of all values in the domain of `var`, ordered according to the least-constraining values heuristic.
- The least-constraining values heuristic is computed as the number of values ruled out for neighboring unassigned variables. 
- Any variable already in the assignment is not counted when computing the number of values ruled out for neighboring unassigned variables.
- For domain values that eliminate the same number of possible choices, any ordering is accepted.

### `select_unassigned_variable`

- Takes the assignment as input and returns a single variable in the crossword that is not yet assigned, according to the minimum remaining value heuristic and then the degree heuristic.
- Returns the variable with the fewest remaining values in its domain. If there is a tie, it chooses the variable with the largest degree (most neighbors). If there is a tie in both cases, it chooses arbitrarily.

### `backtrack`

- Accepts the assignment as input and, using backtrack search, returns a complete satisfactory assignment of variables to values, if possible.
- If a satisfactory crossword puzzle can be generated, returns the complete assignment: a dictionary where each variable is a key and the value is the word for that variable. If no satisfactory assignment is possible, returns `None`.

### `get_arcs`

- A utility function to assist `backtrack`.
- Takes an assignment as input and returns a list of tuples of all overlapping variables not yet in the assignment.

### `queue_2s`

- A utility function to improve the efficiency of `ac3`, by using two stacks (lists) to form a queue.
- Provides a minor improvement, as the queue isn't expected to be large. However, since `ac3` is called frequently inside `backtrack`, it was worth the effort.
```

Feel free to make any additional changes or let me know if there's anything else you'd like to include!