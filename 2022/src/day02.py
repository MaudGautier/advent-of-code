#!/usr/bin/env python3
from typing import List, Tuple, Literal

# Types
OpponentPiece = Literal["A", "B", "C"]
MyPiece = Literal["X", "Y", "Z"]
Outcome = Literal["win", "draw", "loss"]
EncryptedOutcome = Literal["X", "Y", "Z"] # Win, Draw, Loss

# Constants
ROCK = ["A", "X"]
PAPER = ["B", "Y"]
SCISSORS = ["C", "Z"]
WIN = "Z"
DRAW = "Y"
LOSS = "X"
ROCK_PIECE = "A"
PAPER_PIECE = "B"
SCISSORS_PIECE = "C"
# TODO: need to refactor (notably types, to have everything comprehensible and working for both versions - using guide or not)
# MyPiece = Encryption --> either MyEncryptedPiece (no guide) or EncryptedOutcome (with guide)
# Need to compute_piece_score based on ROCK_PIECE, PAPER_PIECE, SCISSORS_PIECE


# Output: [("A", "X"), ("B", "Y"), ("C", "Z")]
def read_data(file_name: str) -> List[Tuple[OpponentPiece, MyPiece]]:
    with open(file_name, 'r') as file:
        lines = [line.strip().split(" ") for line in file.readlines()]
        return [(opponentDraw, myDraw) for [opponentDraw, myDraw] in lines]


def compute_piece_score(piece: MyPiece) -> int:
    if piece in ROCK:
        return 1
    if piece in PAPER:
        return 2
    if piece in SCISSORS:
        return 3


def define_outcome(draw: Tuple[OpponentPiece, MyPiece]) -> Outcome:
    [opponent_piece, my_piece] = draw
    if opponent_piece in ROCK:
        if my_piece in ROCK:
            return "draw"
        if my_piece in PAPER:
            return "win"
        if my_piece in SCISSORS:
            return "loss"
    if opponent_piece in PAPER:
        if my_piece in ROCK:
            return "loss"
        if my_piece in PAPER:
            return "draw"
        if my_piece in SCISSORS:
            return "win"
    if opponent_piece in SCISSORS:
        if my_piece in ROCK:
            return "win"
        if my_piece in PAPER:
            return "loss"
        if my_piece in SCISSORS:
            return "draw"


def compute_outcome_score(outcome: Outcome) -> int:
    if outcome == "win":
        return 6
    if outcome == "draw":
        return 3
    if outcome == "loss":
        return 0


def compute_my_score(draws: List[Tuple[OpponentPiece, MyPiece]]) -> int:
    my_score = 0
    for draw in draws:
        my_piece = draw[1]
        my_score += compute_piece_score(my_piece) + compute_outcome_score(define_outcome(draw))
    return my_score


def decrypt_outcome(encrypted_outcome: EncryptedOutcome) -> Outcome:
    if encrypted_outcome == DRAW:
        return "draw"
    if encrypted_outcome == WIN:
        return "win"
    if encrypted_outcome == LOSS:
        return "loss"


def select_my_piece(draw: Tuple[OpponentPiece, EncryptedOutcome]) -> MyPiece:
    [opponent_piece, encrypted_outcome] = draw
    if opponent_piece in ROCK:
        if encrypted_outcome in WIN:
            return PAPER[0]
        if encrypted_outcome in DRAW:
            return ROCK[0]
        if encrypted_outcome in LOSS:
            return SCISSORS[0]
    if opponent_piece in PAPER:
        if encrypted_outcome in WIN:
            return SCISSORS[0]
        if encrypted_outcome in DRAW:
            return PAPER[0]
        if encrypted_outcome in LOSS:
            return ROCK[0]
    if opponent_piece in SCISSORS:
        if encrypted_outcome in WIN:
            return ROCK[0]
        if encrypted_outcome in DRAW:
            return SCISSORS[0]
        if encrypted_outcome in LOSS:
            return PAPER[0]


def compute_my_score_using_the_guide(draws: List[Tuple[OpponentPiece, EncryptedOutcome]]) -> int:
    my_score = 0
    for draw in draws:
        my_piece = select_my_piece(draw)
        encrypted_outcome = draw[1]
        outcome = decrypt_outcome(encrypted_outcome)
        my_score += compute_piece_score(my_piece) + compute_outcome_score(outcome)
    return my_score



if __name__ == "__main__":
    # ---- TEST DATA -----
    test_data = [
        ("A", "Y"),
        ("B", "X"),
        ("C", "Z")
        ]
    print("-- Tests on test data:")
    print(compute_my_score(test_data) == 15)
    print(compute_my_score_using_the_guide(test_data) == 12)

    # ---- REAL DATA ----
    data = read_data("./2022/data/day02-input.txt")

    # Solution for 2-a
    print("\n-- Solution for 2-a:")
    print(compute_my_score(data)) # 12276

    # Solution for 2-b
    print("\n-- Solution for 2-b:")
    print(compute_my_score_using_the_guide(data)) # 9975

