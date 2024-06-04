# Read me

The problem and it's full description is avaliable in the link: 
https://cs50.harvard.edu/ai/2024/projects/1/knights/

## Introduction:
This problem follow the idea of the the puzzles "knights and Knaves", present in the book "what is the name of this book?" by Raymond Smullyan, 1978.

In a Knights and Knaves puzzle, the following information is given: Each character is either a knight or a knave. A knight will always tell the truth: if knight states a sentence, then that sentence is true. Conversely, a knave will always lie: if a knave states a sentence, then that sentence is false.

The objective of the puzzle is, given a set of sentences spoken by each of the characters, determine, for each character, whether that character is a knight or a knave.

My task in this problem is to determine how to represent these puzzles using propositional logic, such that an AI running a model-checking algorithm could solve these puzzles for us.

## Utilization:
Cd inside knights folder.

run in the terminal: python puzzle.py

The terminal will then show which character of each puzzle is a knight or a Knave


## Understanding:
logic.py is a file premade by Cs50, containing several classes for different types of logical connectives(And, Or, Not, Biconditional, Implication). It also contains the function model_check, that takes a knowledge base and a query, recursively considering all possible models and return True if the knowledge base entails the query, returning false otherwise.

Puzzle.py has four different knowledge bases, knowledge0, knowledge1, knowledge2, knowledge3 which are used to deduce the solution to the puzzles 0, 1, 2 and 3. These knowledge bases were empty and it was my duty to fill them.

## Specifications
In each of the sentences below, each character is either a knight or a knave. Every sentence spoke by a knight is true, every sentence spoke by a knave is false

Obs: Below you will see all knowledge that could be gained based on the phrases said by the character, even those that clearly can't be true. But I am adding them all the same because, in this case, the Ai is the one supposed to do the logical "thinking". 

### Puzzle 0:

A says "I am both a knight and a knave."

### knowledge 0:

One person can be a knight or a knave. Or()

But not both. Not(and())

If he is telling the true, he is a knight. Biconditional(And())

if he is lying, he is a knave. Biconditional(Not(And))

### Puzzle 1:

A says "We are both knaves."

B says nothing.

### Knowledge 1:

One person can be a knight or a knave. Or()

But not both. Not(and())

If A is telling the true, A is a knight. Biconditional(And())

if A is lying, A is a knave. Biconditional(Not(And))

### Puzzle 2:

A says "We are the same kind."

B says "We are of different kinds."

### Knowledge 2:

One person can be a knight or a knave. Or()

But not both. Not(and())

A is a knight, if they are both knights or bot knaves. Biconditional(Or(And(),And()))

A is a knave, if they are of different kinds. Biconditional(Or(And(),And()))

B is a knight, if they are of different kinds. Biconditional(Or(And(),And()))

B is a Knave, if they are both knights or bot knaves. Biconditional(Or(And(),And()))

### Puzzle 3:

A says either "I am a knight." or "I am a knave.", but you don't know which.

B says "A said 'I am a knave'."

B says "C is a knave."

C says "A is a knight."

### knowledge 3:

One person can be a knight or a knave. Or()

But not both. Not(and())

A is a knight if he is either a knight or a Knave. Biconditional(Or())

A is a knave if he is neither a knight or a Knave. Biconditional(Not(Or()))

If B is a knight, then A indeed said that and B is a knave - On which case A is a knight if B is a Knave. Implication(Biconditional())

If B is a knight, then A indeed said that and B is a knave - On which case A is a knave if B is a Knight. Implication(Biconditional())

If B is a Knave, then we can't imply anything, as he could lie by saying the opposite of what A said, or lie saying something A didn't say at all.

B is a knight if C is a knave. Biconditional()

B is a knave if C is a knight. Biconditional()

C is a knight if A is a knight. Biconditional()

C is a knave if A is a knave. Biconditional(),