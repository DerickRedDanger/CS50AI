# Tic-Tac-Toe AI

The full problem description is available [CS50 AI Project 2: Tic-Tac-Toe](https://cs50.harvard.edu/ai/2024/projects/0/tictactoe/).

## Introduction

This project's objective is to create a weak AI (rule-based AI that cannot adapt/learn) that always makes optimal moves in a Tic-Tac-Toe game. Since optimal play in Tic-Tac-Toe results in a tie, you shouldn't be able to beat the AI.

## Usage

1. Navigate to the `tictactoe` folder.
2. Run the following command in the terminal to install the required packages (only needed once):
   ```
   pip3 install -r requirements.txt
   ```
3. Run the game using the command:
   ```
   python runner.py
   ```
4. Choose if you want to play as X or O and play against the AI.

## Understanding the Code

### runner.py

This file was implemented by CS50 and contains all the code to run the graphical interface of the game.

### tictactoe.py

This file contains all the AI's logic. Only the `initial_state` function and the designations for X, O, and Empty were provided by CS50. The implementation of the functions `player`, `actions`, `result`, `winner`, `terminal`, `utility`, and `minimax` were done by me. Additionally, the `optimal` function was created to facilitate debugging and help in the creation of `minimax`.

## Specifications

### Player Function
Takes a board as an argument and returns which player will be next. It generates an error if it finds that invalid moves were made.

### Actions Function
Takes a board as an argument and returns a set of all possible actions (row, column) on that board.

### Result Function
Takes a board and an action as arguments, calls the `player` function on execution, and returns the board that would result from said player's action (playing in a given row/column). Raises an error if an invalid move is made.

### Winner Function
Takes a board as input and checks if there are three moves in a row from the same player. If there is, it returns that player (X or O). Otherwise, it returns None.

### Terminal Function
Takes a board as input and checks if the game is over, whether because there’s a winner or because there’s no more empty space. If the game ends, it returns True; otherwise, it returns False.

### Utility Function
Helps in the creation of the AI. It takes a terminal board (will only be called on a board where the game has already ended) and returns this board's utility. It returns 1 if X won, -1 if O won, and 0 if it was a tie.

### Minimax Function
Takes the current game board and returns the optimal action for the current AI player on the board, but returns None if it's a terminal board.

This is done by taking all the currently available moves and passing them as arguments to the `optimal` function (explained below), which will return each move's utility. These moves are then separated based on their utility.

The AI then picks a move of the best-suited utility for them (if available). If AI is an X player, it will randomly (for variety) pick a move from the moves with utility 1; if none are available, it will pick randomly from the utility 0; else it will pick randomly from utility -1. If AI is an O player, it will start from -1, then 0, then 1.

### Optimal Function
Takes a board and an action, then checks the result of this board and action. If it's terminal, it returns this board's utility.

If it's not terminal, it will check whose turn it is, find all actions available on the board from the result, and recursively call itself, checking each option until reaching a terminal board.

Upon finding a terminal board and finding its utility, it will return the utility to the previous `optimal`. If this action would result in the victory of the current player, it will stop searching and return it (since this player would play optimally and try to win). Otherwise, it will continue searching and return the most optimal value for the current player. 

This AI checks all possible future actions that an initial action could lead to, picks the path on which both players would play optimally, and values the current move based on the final result of this path.

### Example 1 of `optimal` function

Take the board and action below as an example of arguments to `optimal`.

**Argument:** 
```
[[X, X, EMPTY], [O, O, EMPTY], [X, EMPTY, EMPTY]], (2, 1)
```

Since this is O's turn, this would lead to the following result. Since this is not a terminal board and we still don't know the results to which this board would lead, its utility is unknown.

```
Result: [[X, X, EMPTY], [O, O, EMPTY], [X, O, EMPTY]], Utility ?
```

Now it would be X's turn. Looking at all possible moves, we'd get the following results and utilities:

```
Option 1: [[X, X, EMPTY], [O, O, X], [X, O, EMPTY]], Utility ?
Option 2: [[X, X, EMPTY], [O, O, EMPTY], [X, O, X]], Utility ?
Option 3: [[X, X, X], [O, O, EMPTY], [X, O, EMPTY]], Utility 1
```

Since we are considering that both sides always play optimally and it's X's turn, they would always try to maximize their utility. Since the highest utility possible is 1, between the three options, X would choose the last as it would lead to their win. Because of this, we can backtrack and consider that the utility of the input to `optimal` also has a utility of 1 since playing optimally would lead to that outcome.

```
Result: [[X, X, EMPTY], [O, O, EMPTY], [X, O, EMPTY]], Utility 1
```

So `optimal` would return that the action `(2,1)` has a utility of 1. And since it was O's turn, O will pick an action that would lead to -1 first, then 0, and only if none other is available, 1.

### Example 2 of `optimal` function

If the action above didn't lead to a terminal board, it would be passed to the `optimal` function again, and all possible actions and their results would be examined. To exemplify that, let's consider that Option 1 was the initial input to the `optimal` function.

```
Option 1: [[X, X, EMPTY], [O, O, X], [X, O, EMPTY]], Utility ?
Renaming it to avoid confusion:
Result: [[X, X, EMPTY], [O, O, X], [X, O, EMPTY]], Utility ?
```

Being O's turn, it would lead to both of these actions.
```
1º move:
Option 1: [[X, X, O], [O, O, X], [X, O, EMPTY]], Utility ?
Option 2: [[X, X, EMPTY], [O, O, X], [X, O, O]], Utility ?
```

Which, on X's turn, would lead to:
```
2º move:
Option 1-1: [[X, X, O], [O, O, X], [X, O, X]], Utility 0
Option 2-1: [[X, X, X], [O, O, X], [X, O, O]], Utility 1
```

Now that we have the utility of both outcomes, we can backtrack and find which path the AI would take.

Since there are no actual options of movement past the first move, their utility is that of the only possible outcome they got.

So the 1st move option's utility is the following:
```
1º move:
Option 1: [[X, X, O], [O, O, X], [X, O, EMPTY]], Utility 0
Option 2: [[X, X, EMPTY], [O, O, X], [X, O, O]], Utility 1
```

On the first move, the AI has two options of movement, one with utility 0 and one with utility 1. It will look at the utility of the possible outcomes and decide based on which player's turn it is.

Since it's O's turn, it will try to minimize the score, so it will pick the option with the lowest utility, in other words, Option 1.

```
Result: [[X, X, EMPTY], [O, O, X], [X, O, EMPTY]], Utility 0
```

Which means that the action used as an argument to this `optimal` function has the utility of 0 too. Since if both players play optimally, it would lead to the following outcome:

```
Result: [[X, X, EMPTY], [O, O, X], [X, O, EMPTY]], Utility 0
                    |
                    v
Option 1: [[X, X, O], [O, O, X], [X, O, EMPTY]], Utility 0
                    |
                    v
Option 1-1: [[X, X, O], [O, O, X], [X, O, X]], Utility 0
```

Thus, for this input, `optimal` would return the action `(1,2)` and the utility 0.

### Observation
It would be possible to encourage the AI to go for quicker wins by increasing the range of return values in `utility`. 

For example, instead of just using 1 for X's win and -1 for O's win, we could reduce the number of turns taken from these values. If X wins in 5 turns, it would return 0.5; if it wins in 7 turns, it would return 0.3. If O wins in 6 turns, it would return -0.4, and -0.2 in 8 turns. Since it always takes 9 moves for a tie, this value would never reach 0.

Considering the simplicity of the game, I expect the difference in the AI's behavior to be minor. Since CS50 specified that `utility` should return 1, 0, or -1, I didn't actually try it.

