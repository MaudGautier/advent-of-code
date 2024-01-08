from typing import List, Tuple, Literal, Dict, Type, Union


class Category:
    text: str


a = Category()
a.text = 1.5454654  # where is the warning?

# Constants
ROCK = ["A", "X"]
PAPER = ["B", "Y"]
SCISSORS = ["C", "Z"]
WIN = "Z"
TIE = "Y"
LOSS = "X"
ROCK_PIECE: Literal["A"] = "A"
PAPER_PIECE = "B"
SCISSORS_PIECE = "C"

# Types
OpponentPiece = Literal[ROCK_PIECE, PAPER_PIECE, SCISSORS_PIECE]
MyPiece = Literal["X", "Y", "Z"]
Outcome = Literal["win", "draw", "loss"]

# 2-a
EncryptedInformation: Union["X", "Y", "Z"] = Literal["X", "Y", "Z"]
Piece = Literal[ROCK_PIECE, "B"]

PIECE_DECRYPTOR: Dict[EncryptedInformation, Piece] = {
    "X": "Xaaa"
}

# 2-b
EncryptedOutcome = Literal[ROCK_PIECE, PAPER_PIECE, SCISSORS_PIECE]  # Loss, Draw, Win


# TODO: need to refactor (notably types, to have everything comprehensible and working for both versions - using guide or not)
# MyPiece = Encryption --> either MyEncryptedPiece (no guide) or EncryptedOutcome (with guide)
# Need to compute_piece_score based on ROCK_PIECE, PAPER_PIECE, SCISSORS_PIECE


# Output: [("A", "X"), ("B", "Y"), ("C", "Z")]
def read_data(file_name: str) -> List[Tuple[OpponentPiece, EncryptedInformation]]:
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


# OUTCOME_GUIDE = {
#     ROCK_PIECE: {WIN: PAPER_PIECE, TIE: ROCK_PIECE, LOSS: SCISSORS_PIECE},
#     PAPER_PIECE: {WIN: SCISSORS_PIECE, TIE: PAPER_PIECE, LOSS: ROCK_PIECE},
#     SCISSORS_PIECE: {WIN: ROCK_PIECE, TIE: SCISSORS_PIECE, LOSS: PAPER_PIECE}
# }


def define_outcome(draw: Tuple[OpponentPiece, MyPiece]) -> Outcome:
    [opponent_piece, my_piece] = draw
    if opponent_piece == ROCK_PIECE:
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


def decrypt_piece_without_guide(encrypted_information: EncryptedInformation) -> Piece:
    return 0


def compute_my_score_without_guide(draws: List[Tuple[OpponentPiece, EncryptedInformation]]) -> int:
    my_score = 0
    for draw in draws:
        encrypted_information = draw[1]
        my_piece = decrypt_piece_without_guide(encrypted_information)
        my_score += compute_piece_score(my_piece) + compute_outcome_score(define_outcome(draw))
    return my_score


def decrypt_outcome(encrypted_outcome: EncryptedOutcome) -> Outcome:
    if encrypted_outcome == TIE:
        return "draw"
    if encrypted_outcome == WIN:
        return "win"
    if encrypted_outcome == LOSS:
        return "loss"


GUIDE = {
    ROCK_PIECE: {WIN: PAPER_PIECE, TIE: ROCK_PIECE, LOSS: SCISSORS_PIECE},
    PAPER_PIECE: {WIN: SCISSORS_PIECE, TIE: PAPER_PIECE, LOSS: ROCK_PIECE},
    SCISSORS_PIECE: {WIN: ROCK_PIECE, TIE: SCISSORS_PIECE, LOSS: PAPER_PIECE}
}


def select_my_piece(draw: Tuple[OpponentPiece, EncryptedOutcome]) -> MyPiece:
    [opponent_piece, encrypted_outcome] = draw
    return GUIDE[opponent_piece][encrypted_outcome]


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
    print(compute_my_score_without_guide(test_data) == 15)
    print(compute_my_score_using_the_guide(test_data) == 12)

    # ---- REAL DATA ----
    data = read_data("./data/2022/day02-input.txt")

    # Solution for 2-a
    print("\n-- Solution for 2-a:")
    print(compute_my_score_without_guide(data))  # 12276

    # Solution for 2-b
    print("\n-- Solution for 2-b:")
    print(compute_my_score_using_the_guide(data))  # 9975

# TODO: add complexity
