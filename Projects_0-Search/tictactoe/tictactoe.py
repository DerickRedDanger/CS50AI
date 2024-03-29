import copy
import random
"""
Tic Tac Toe Player
"""
X = "X"
O = "O"
EMPTY = None

N = 0
# List used on both winner and terminal functions
winning_conditions = [
    [(0, 0), (0, 1), (0, 2)],  # top row
    [(1, 0), (1, 1), (1, 2)],  # middle row
    [(2, 0), (2, 1), (2, 2)],  # bottom row
    [(0, 0), (1, 0), (2, 0)],  # left column
    [(0, 1), (1, 1), (2, 1)],  # middle column
    [(0, 2), (1, 2), (2, 2)],  # right column
    [(0, 0), (1, 1), (2, 2)],  # main diagonal
    [(0, 2), (1, 1), (2, 0)]  # secondary diagonal
]


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # ---- TODO ----
    Nx = 0
    No = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == X:
                Nx += 1
            elif board[i][j] == O:
                No += 1

    if Nx == 0 and No == 0:
        return X
    elif Nx == (No + 1):
        return O
    elif Nx == No:
        return X
    else:
        raise NameError("Invalid Moves were made")

    raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # ---- TODO ----
    Terminal = terminal(board)
    if Terminal:
        raise NameError("The game ended, but action was still called")
    action = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                action.append((i, j))
    action = set(action)
    return action

    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # ---- TODO ----
    Player = player(board)
    Board = copy.deepcopy(board)
    if 2 >= action[0] >= 0 and 2 >= action[1] >= 0:
        if Board[action[0]][action[1]] != EMPTY:
            raise NameError("Invalid move")
        else:
            Board[action[0]][action[1]] = Player
            return Board
    else:
        raise NameError("Invalid move")
    raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # ---- TODO ----
    for first, second, third in winning_conditions:
        if board[first[0]][first[1]] == board[second[0]][second[1]] == board[third[0]][third[1]] != EMPTY:
            return board[first[0]][first[1]]
    return None
    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # ---- TODO ----
    for first, second, third in winning_conditions:
        if board[first[0]][first[1]] == board[second[0]][second[1]] == board[third[0]][third[1]] != EMPTY:
            return True

    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                return False
    return True

    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    global N
    N += 1
    # ---- TODO ----
    # This function will only be called when a terminal(board) returns true
    # so the game is already over. Thus, if neither side won, it's a tie
    for first, second, third in winning_conditions:
        if board[first[0]][first[1]] == board[second[0]][second[1]] == board[third[0]][third[1]] != EMPTY:
            if board[first[0]][first[1]] == X:
                return 1
            elif board[first[0]][first[1]] == O:
                return -1

    return 0

    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # ---- TODO ----
    if terminal(board):
        return None
    else:
        Player = player(board)
        Actions = actions(board)
        options = []
        moves_1 = []
        moves_0 = []
        moves__1 = []
        for i in Actions:
            options.append(i)

        for j in options:
            x = optimal(board, j)
            if x == 1:
                moves_1.append(j)
            if x == 0:
                moves_0.append(j)
            if x == -1:
                moves__1.append(j)

        if Player == X:
            move = None
            if moves_1:
                move = random.choice(moves_1)
            elif moves_0:
                move = random.choice(moves_0)
            elif moves__1:
                move = random.choice(moves__1)
            return move

        elif Player == O:
            move = None
            if moves__1:
                move = random.choice(moves__1)
            elif moves_0:
                move = random.choice(moves_0)
            elif moves_1:
                move = random.choice(moves_1)
            return move

    raise NotImplementedError


def optimal(board, Action):

    Board = copy.deepcopy(board)
    Result = result(Board, Action)
    if terminal(Result):
        return utility(Result)
    else:
        Player = player(Result)

        if Player == X:
            best = -float('inf')
            for i in actions(Result):

                value = optimal(Result, i)
                best = max(best, value)

            return best

        if Player == O:
            best = float('inf')
            for i in actions(Result):
                value = optimal(Result, i)
                best = min(best, value)

            return best
