from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")
"""""
# Puzzle 0
# A says "I am both a knight and a knave."
"""""
knowledge0 = And(
    # TODO

    # One person can be a knight or a knave,
    Or(AKnight, AKnave),
    # But not both
    Not(And(AKnight, AKnave)),

    # If he is telling the truth, he is a Knight.
    Biconditional(AKnight, And(AKnight, AKnave)),
    # If he is lying, he is a Knave
    Biconditional(AKnave, Not(And(AKnight, AKnave)))
)

# -----------------------------------------------------
"""""
# Puzzle 1
# A says "We are both knaves."
# B says nothing.
"""""
knowledge1 = And(
    # TODO

    # One person can be a knight or a knave,
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    # But not both
    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),

    # If A is telling the true, he is a Knight,
    Biconditional(AKnight, And(AKnave, BKnave)),
    # else, he is a knave
    Biconditional(AKnave, Not(And(AKnave, BKnave))),
)

# -----------------------------------------------------
"""""
# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
"""""
knowledge2 = And(
    # TODO

    # One person can be a knight or a knave,
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    # But not both
    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),

    # A is a knight if they are both Knights or both knave
    Biconditional(AKnight, Or(And(AKnave, BKnave), And(AKnight, BKnight))),

    # A is a knave if they are of different kinds
    Biconditional(AKnave, Or(And(AKnight, BKnave), And(AKnave, BKnight))),

    # B is a knight if they are of different kinds
    Biconditional(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight))),

    # B is a knave if they are both Knights or knave
    Biconditional(BKnave, Or(And(AKnave, BKnave), And(AKnight, BKnight))),
)

# -----------------------------------------------------
"""""
# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
"""""
knowledge3 = And(
    # TODO

    # One person can be a knight or a knave,
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Or(CKnight, CKnave),
    # But not both
    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),
    Not(And(CKnight, CKnave)),

    # A is a knight if he is either a knight or a Knave
    Biconditional(AKnight, Or(AKnight, AKnave)),

    # A is a knave if he is neither a knight or a Knave
    Biconditional(AKnave, Not(Or(AKnight, AKnave))),

    # If B is a knight, then A indeed said that and B is a knave - On which case A is a knight if B is a Knave
    Implication(BKnight, Biconditional(AKnight, BKnave)),

    # If B is a knight, then A indeed said that and B is a knave - On which case A is a knave if B is a Knight
    Implication(BKnight, Biconditional(AKnave, BKnight)),

    # if B is a Knave, then we can't imply anything, as he could lie by saying the opposite of what A said,
    # or lie saying something A didn't say at all.

    # B is a knight if C is a knave
    Biconditional(BKnight, CKnave),

    # B is a knave if C is a knight
    Biconditional(BKnave, CKnight),

    # C is a knight if A is a knight
    Biconditional(CKnight, AKnight),

    # C is a knave if A is a knave
    Biconditional(CKnave, AKnave),
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
