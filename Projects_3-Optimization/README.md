The problem and it's full description is avaliable in the link: 
https://cs50.harvard.edu/ai/2024/projects/3/crossword/

## Introduction:

This project aims at creating an Ai capable of generating+ a crossword, given a file representing the structure the crossword should assume and a file containing all words available for use.

It will read the structure file, recognizing the space for the words, it's length, direction and at which points it overlaps with another word. After that, for each variable, it will create a domain containing all words in the words file, then remove those that don't fit that variable's length.

Finally, it will loop in each variable, trying the available words and back tracking if it didn't work, until all words fit the limitations.

To optimize the process, it will prioritize the unassigned variable with the least amount of words remaining, using as tiebreaker the variable that overlaps the most. As for the words, for each variable, it will try them in the order of the least constraining word, in other words, the words that will eliminate the least amount of words from it's overlapping variables when chosen.

The limitation chosen for this crossword is that each word must be unique.

## Utilization:

* cd inside crossword

* run in the terminal: python generate.py data/structure.txt data/words.txt (where both structure and words can be 1,2 or 3. You can also create your own structure or word file.)

* If it's possible to create a crossword with that structure and words, the terminal will show the representation of the crossword. If it's nor possible, it will return 'No Solution'.

* If you'd like, it's possible to generate a png representing the crossword (You might need to run pip3 install pillow, if you didn't already). that's done by adding output.png at the end of the command line. For example: python generate.py data/structure1.txt data/words1.txt output.png

## Background:

How might you go about generating a crossword puzzle? Given the structure of a crossword puzzle (i.e., which squares of the grid are meant to be filled in with a letter), and a list of words to use, the problem becomes one of choosing which words should go in each vertical or horizontal sequence of squares. We can model this sort of problem as a constraint satisfaction problem. Each sequence of squares is one variable, for which we need to decide on its value (which word in the domain of possible words will fill in that sequence). 

As with many constraint satisfaction problems, these variables have both unary and binary constraints. The unary constraint on a variable is given by its length. The binary constraints on a variable are given by its overlap with neighboring variables. 

For each pair of neighboring variables, those variables share an overlap: a single square that is common to them both. We can represent that overlap as the character index in each variable’s word that must be the same character. 

For this problem, we’ll add the additional constraint that all words must be different: the same word should not be repeated multiple times in the puzzle.

The challenge was, then, to write a program to find a satisfying assignment: a different word (from a given vocabulary list) for each variable such that all the unary and binary constraints are met.

## Understanding:

This project is composed of the files crossword.py, generate.py and the directory data. 

Crossword.py was fully implemented by Cs50, it contains the base of the crossword, that being the class crossword (being the puzzle itself) and the class variable (representing a variable in the crossword).

The directory data contains the words and structures that were used to make and test this project, but you are free to create your own. Notice in a structure_file, he '_' represents a blank cell (a space for a letter), any other character represents a cell that won't be filled. Words_file defines a list of words (one per line) to use for the vocabulary of the puzzle.

Generate.py contains the logic of this project. Here, Cs50 defined the class CrosswordCreator that will be used to solve the crossword puzzle. It also comes with the Print function (the one responsible for showing the solution in the terminal), Save is the function that can generate an image file corresponding to that solution (need: pip3 install pillow), letter_grid is a helper function used by both print and save, it generates a 2d list of all characters i their appropriated positions for a given solution.

Finally, the Solve function does three things: It calls enforce_node_consistency to enforce node consistency on the crossword puzzle, ensuring that every value in a variable’s domain satisfy the unary constraints. Next, the function calls ac3 to enforce arc consistency, ensuring that binary constraints are satisfied. Finally, the function calls backtrack on an initially empty assignment (the empty dictionary dict()) to try to calculate a solution to the problem.

My task was to complete the implementation of enforce_node_consistency, revise, ac3, assignment_complete, consistent, order_domain_values, selected_unassigned_variable, and backtrack in generate.py. I also implemented the queue_2s and get_arcs functions to assist my functions.

## Specification:

### enforce_node_consistency:
* Updates self.domains, such that each variable's domains are node consistent.
* In the case of a crossword puzzle, this means making sure each value in a variable's domain has the same number of letters as the variable's length.

### revise:
* Take as input two variables (X, Y) and enforce arc consistence between them.
* x is arc consistent with y when every value in the domain of x has a possible value in the domain of y that does not cause a conflict. (A conflict in the context of the crossword puzzle is a square for which two variables disagree on what character value it should take on.)
* the domain of Y was left unmodified, only X was edited.
* The function returns True if an update was made to the domain of x; it should return False if no revision was made.

### ac3:
* Enforces arc consistency across all arcs given as input.

* Takes arcs as input (list of tuples made of two variables (x,y)) and enforces arc consistence on them. If no arcs were given, enforces arc consistence on all overlapping variables

* this is done by queuing each ark, passing both of them to revise and, if x was updated, queuing tuples all other variables that overlap with x and them (z,x).

* that queue was made utilizing the queue_2s function that simulates a queue using two stacks.

* if during this process all values of a variable's domain are removed, returns False, meaning it's impossible to solve the problem, since there are no more possible values for the variable.

* word uniqueness wasn't enforced here, it was implemented in the consistent function.

### assignment_complete:

* This function takes an assignment dictionary, where each key is a variable object that is already in use in crosswordcreater while the value is the word that variable tool. Any variable yet unassigned won't be in this dictionary.

* this function checks if a given assignment is completed. This is true if all variables are in the dictionary and have a value (regardless of what their value is.)

* This functions returns True if the assignment is complete, false otherwise.

### consistent:

* This functions checks if a given assignment is consistent

* it's consistent if it satisfies all the constraints of the problem: that is to say, all values are distinct, every value is the correct length, and there are no conflicts between neighboring variables.

* Returns True if it's consistent, False otherwise

### order_domain_values:

* takes as input a variable var and current assignments.

* returns a list of all values in the domain of var, ordered according to the least-constraining values heuristic

* least-constraining values heuristic is computed as the number of values ruled out for neighboring unassigned variables. That is to say, if assigning var to a particular value results in eliminating n possible choices for neighboring variables, you should order your results in ascending order of n.

* any variable already present in assignment already has a value, so it's not counted when computing the number of values ruled out for neighboring unassigned variables.

* for domain values that eliminate the same number of possible choices, any ordering is accepted.

### select_unassigned_variable:

* takes assignment as input and returns a single variable in the crossword that is not yet assigned to assignment, according to the minimum remaining value heuristic and then the degree heuristic.

* it returns the variable with the fewest number of remaining values in its domain. If there is a tie between variables, it chooses the variable that has the largest degree (has the most neighbors). If there is a tie in both cases, it chooses arbitrarily between them.

### backtrack:

* accepts backtrack as input and, using backtrack search, returns a complete satisfactory assignment of variables to values, if it is possible to do so.

* If it is possible to generate a satisfactory crossword puzzle, the function returns the complete assignment: a dictionary where each variable is a key and the value is the word that the variable should take on. If no satisfying assignment is possible, the function returns None.

### get_arcs:

* a utility function made to assist backctrack

* it takes an assignment as input and return a list of tuples of all overlapping variables that aren't yet in the assignment.

### queue_2s:

* a utility function made to improve the efficiency of ac3, by using two stacks (lists) to form a queue, instead of using a queue itself.

* don't expect a big improvement, considering the queue isn't expected to be big. But since ac3 is called frequently inside backtrack, it still felt worth the effort.