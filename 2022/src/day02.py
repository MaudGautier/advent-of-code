#!/usr/bin/env python3
from typing import List, Tuple, Literal

# Types
OpponentPiece = Literal["A", "B", "C"]
MyPiece = Literal["X", "Y", "Z"]
Outcome = Literal["draw", "win", "loss"]

# Constants
ROCK = ["A", "X"]
PAPER = ["B", "Y"]
SCISSORS = ["C", "Z"]


# Output: [("A", "X"), ("B", "Y"), ("C", "Z")]
def read_data(file_name: str) -> List[Tuple[OpponentPiece, MyPiece]]:
    with open(file_name, 'r') as file:
        lines = [line.strip().split(" ") for line in file.readlines()]
        return [(opponentDraw, myDraw) for [opponentDraw, myDraw] in lines]


def compute_piece_score(piece: MyPiece) -> int:
    if piece == "X":
        return 1
    if piece == "Y":
        return 2
    if piece == "Z":
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


def compute_outcome_score(draw: Tuple[OpponentPiece, MyPiece]) -> int:
    if define_outcome(draw) == "win":
        return 6
    if define_outcome(draw) == "draw":
        return 3
    if define_outcome(draw) == "loss":
        return 0


def compute_my_score(draws: List[Tuple[OpponentPiece, MyPiece]]) -> int:
    my_score = 0
    for draw in draws:
        my_score += compute_piece_score(draw[1]) + compute_outcome_score(draw)
    return my_score


if __name__ == "__main__":
    # ---- TEST DATA -----
    test_data = [
        ("A", "Y"),
        ("B", "X"),
        ("C", "Z")
        ]
    # Solution for 1-a
    print(compute_my_score(test_data) == 15)

    # ---- REAL DATA ----
    data = read_data("./2022/data/day02-input.txt")
    # Solution for 1-a
    print(compute_my_score(data))

