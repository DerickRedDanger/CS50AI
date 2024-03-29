The problem and it's full description is avaliable in the link: https://cs50.harvard.edu/ai/2024/projects/0/tictactoe/

* Introduction:

This project's objective is to create a weak Ai (Rule based Ai, one that can't adapt/learn) that always make optimal moves in a Tic Toc Toe game. Since optimal plays in a Tic Toc Toe result in a tie, You shouldn't be able to beat the Ai.

* Utilization:

cd inside Tictactoe folder.

Run in the terminal: pip3 install -r requirements.txt. You only need to do this once.

Run in the terminal: python runner.py

Choose if you want to play as X or O and play against the Ai.

* Understanding:

There are two Main files in this Project.

Runner.py was implemented by Cs50 and contains all the the code to run the graphical interface of the game.

tictacttoe.py contains all the Ai's logic. Only the function initial_state and the designitaion of X, O and Empty were made by Cs50.

The implementation of the functions player, actions, result, winner, terminal, utility and minimax were made by me.

The function optimal was made to facilitate debugging and helping in the create of minimax.

* Specification:

player function: Takes a board as arguments (even hypothetical ones) and returns which player will be next. It generates an error if it finds that invalid movements were made.

action function : Takes a board as an argument and returns a set of all possible actions (row, column) on that board.

result function: takes a board and an action as arguments, calls the player function on execution and returns the board that would result from said player's action (playing in a given row/column). Raises an error if an invalid move is made.

winner function: Takes a board as input and check and checks if there are three moves in a row from either of the player. If there is, return that player (X or O). Else, return None.

terminal function: Takes a board as input and checks if the game is over. Whether it’s because there’s a winner or because there’s no more empty space. If the game ends, it returns True, otherwise it returns False

utility function: Function made to help in the creation of the Ai, it takes a terminal board (will only be called on a board where the game already ended) and return this board's utility. Returning 1 if X won, -1 if O won and 0 if it was a tie.

Function minimax: This function takes the current game board and returns the optimal action for the current Ai player on the board, but returns None if it's a terminal board.

    This is done by taking all the currently avaliable moves and passing them as arguments to the optimal function (explained below), which will return each move's utility. These moves are then separated based on their utility.

    The Ai then pick a move of the best suited utility for then (if avaliable). If Ai is a X player, it will randomly (for variety) pick a move from the Moves with utility 1, if none are avaliable, it will pick a random from the utility 0, else it will pick a random from utility -1. If Ai is a O player, it will start from -1, then 0 then 1.
    
Function optimal: This function takes a board and a action. then check the result of this board and action. If it's terminal, it return this board utility.

    If it's nor terminal, it will check whose the turn is, find all actions avaliable on the board from result and recursively call itself, checking each option till reaching a terminal board.

    Upon finding a terminal board, and find it's utility, it will return the utility to the previous optimal. If this action would result in the victory of the current player it will stop searching and return it (since this player would play optimally and try to win), else, it would continue searching and return the most optimal value to the current player. This happens because we do not save the actions (since the opposing player could make a different moviment then expected) but only the result that would come from this moviment, if both sides played optimally.

    That's to say, this Ai check all possible future actions that a initial action could lead to, picks the path on which both player would play optimally and value this moviment based on the final result of this path.

* Example 1 of optimal function

    Take the board and action Below as an example of arguments to optimal.
    argument: [[X,X,Empty], [O,O,Empty], [X,Empty,Empty]] , (2,1)

    Since this is O's turn, this would lead to the following result. Since this is not a terminal board and we still don't know the results to which this board would lead, it's utility is unknow.
    Result: [[X,X,Empty], [O,O,Empty], [X,O,Empty]] , Utility ?

    Now it would be X turn, looking at all possible moves, we'd get the following results and utility.

    Option 1: [[X,X,Empty], [O,O,X], [X,O,Empty]] , Utility ?

    Option 2: [[X,X,Empty], [O,O,Empty], [X,O,X]] , Utility ?

    Option 3: [[X,X,X], [O,O,Empty], [X,O,Empty]] , Utility 1

    Since we are considering that both sides always play optimally and it's X's turn, he would always try to maximise it's utility. Since the highest utility possible is 1, between the 3 options, X would choose the last, as it would lead to it's win. And because of it, we can backtrack and consider that the utility of the input to optimal also have a utility of 1, since playing optimally, it would lead to that outcome.

    Result: [[X,X,Empty], [O,O,Empty], [X,O,Empty]] , Utility 1

    So optimal would return that the action (2,1) has a utility of 1. And since it was O's turn, O will pick a action that would lead to -1 first, then 0, and only if no other is avaliable, 1.

* Example 2 of optimal function

    if the action above didn't led to a terminal board, it would be passed to the optimal function again and all possible actions and it's result would be examined. to exemplify that, let's consider the options 1 of moviment.

    Option 1: [[X,X,Empty], [O,O,X], [X,O,Empty]] , Utility ?

    Renaming it to avoid confusion:

    Result: [[X,X,Empty], [O,O,X], [X,O,Empty]] , Utility ?

    Being O's turn, it would lead to both of theses actions.

    1º move:

    Option 1: [[X,X,O], [O,O,X], [X,O,Empty]] , Utility ?

    Option 2: [[X,X,Empty], [O,O,X], [X,O,O]] , Utility ?

    Which, on X's, would lead to:

    2º move:

    Option 1 - 1: [[X,X,O], [O,O,X], [X,O,X]] , Utility 0

    Option 2 - 1: [[X,X,X], [O,O,X], [X,O,O]] , Utility 1

    Now that we got the utility of both outcomes, we can back tracking and find which Path the Ai would take.

    Since there is not actual option of moviment past the first move, their utility is that of the only possible outcome they got.

    so the 1° move option's utility is the following

    1º move:

    Option 1: [[X,X,O], [O,O,X], [X,O,Empty]] , Utility 0

    Option 2: [[X,X,Empty], [O,O,X], [X,O,O]] , Utility 1

    On the first move, the Ai have two options of moviment, one with utility 0 and one with utility 1, so he will look at the utility of the possible outcomes and decide based on which player's turn it. 
    
    Since it's O's turn, it will try to minimize the score, so he'd pick the option with the lowest utility. in other words the option 1.

    Result: [[X,X,O], [O,O,X], [X,O,Empty]] , Utility 0

    which means that the action used as argument to this optimal function has the utility of 0 too. Since if both players play optimally, it would lead to the following outcome.

    Result: [[X,X,O], [O,O,X], [X,O,Empty]] , Utility 0

                        |
                        v

    Option 1: [[X,X,O], [O,O,X], [X,O,Empty]] , Utility 0

                        |
                        v

    Option 1 - 1: [[X,X,O], [O,O,X], [X,O,X]] , Utility 0

    Thus, to this input, Optimal would return the action (1,2) and the utility 0.