#!/usr/bin/env python3
from typing import List, Tuple, NamedTuple

Board = List[List[int]]
Cards = List[int]
Draws = List[int]


class BingoBoardResult(NamedTuple):
    winning_index: int
    last_draw: int
    unmarked_cards: Cards


MARKED_CARD = -1


# Data file contains list of drawn numbers on the first line and boards on all following lines
def read_data(file_name: str) -> Tuple[Draws, List[Board]]:
    with open(file_name, "r") as file:
        sections = file.read().strip().split("\n\n")

    draws = [int(draw) for draw in sections[0].split(",")]

    boards = []
    for section in sections[1:]:
        string_rows = section.split("\n")
        board = []
        for string_row in string_rows:
            row = [int(cell) for cell in string_row.split()]
            board.append(row)
        boards.append(board)

    return draws, boards


# Marks board by replacing all occurrences of draw by -1
def mark_board(board: Board, draw: int) -> Board:
    for row_index, row in enumerate(board):
        for cell_index, cell in enumerate(row):
            if cell == draw:
                board[row_index][cell_index] = -1

    return board


# Board is won if one row or one column contains only MARKED_CARD values
def is_board_won(board: Board) -> bool:
    # Check rows
    for row in board:
        if set(row) == {MARKED_CARD}:
            return True
    # Check columns
    for column_index in range(len(board[0])):
        column_values = [
            board[row_index][column_index] for row_index, row in enumerate(board)
        ]
        if set(column_values) == {MARKED_CARD}:
            return True

    return False


# Extract all cards that are not MARKED_CARD
def extract_unmarked_cards_from_board(board: Board) -> Cards:
    unmarked_cards = []
    for row in board:
        for card in row:
            if card != MARKED_CARD:
                unmarked_cards.append(card)

    return unmarked_cards


# Play (i.e. continue marking drawn values on board) until the board is won
def win_board(draws: Draws, board: Board) -> BingoBoardResult:
    for draw_index, draw in enumerate(draws):
        board = mark_board(board, draw)
        if is_board_won(board):
            break

    remaining_unmarked_cards = extract_unmarked_cards_from_board(board)
    return BingoBoardResult(
        winning_index=draw_index,
        last_draw=draw,
        unmarked_cards=remaining_unmarked_cards,
    )


def extract_nth_winning_board(
    bingo_results: List[BingoBoardResult], nth_winning_board: int
) -> BingoBoardResult:
    sorted_bingo_results = sorted(bingo_results, key=lambda x: x.winning_index)
    return sorted_bingo_results[nth_winning_board]


def play_bingo(draws: Draws, boards: List[Board]) -> List[BingoBoardResult]:
    results = []
    for board in boards:
        bingo_board_results = win_board(draws, board)
        results.append(bingo_board_results)

    return results


def calculate_board_score(last_drawn_number: int, unmarked_cards: Cards) -> int:
    return sum(unmarked_cards) * last_drawn_number


if __name__ == "__main__":
    # Tests
    print("-- Tests on `is_board_won` function")
    board_not_won = [[0] * 5 for cell in range(0, 5)]
    board_won_by_row = [[0] * 5 for cell in range(0, 4)] + [[-1] * 5]
    board_won_by_column = [[0, -1, 0, 0, 0] for cell in range(0, 5)]
    print(is_board_won(board_not_won) == False)
    print(is_board_won(board_won_by_row) == True)
    print(is_board_won(board_won_by_column) == True)

    # Test data
    print("\n-- Tests on test data:")
    (test_draws, test_boards) = read_data("./2021/day04-input-test.txt")
    test_bingo_results = play_bingo(test_draws, test_boards)
    test_winner_board = extract_nth_winning_board(test_bingo_results, 0)
    test_winner_board_score = calculate_board_score(
        test_winner_board.last_draw, test_winner_board.unmarked_cards
    )
    print(test_winner_board_score == 4512)

    # Solution for 4-a
    print("\n-- Solution for 4-a:")
    (draws, boards) = read_data("./data/2021/day04-input.txt")
    bingo_results = play_bingo(draws, boards)
    winning_board = extract_nth_winning_board(bingo_results, 0)
    winning_board_score = calculate_board_score(
        winning_board.last_draw, winning_board.unmarked_cards
    )
    print("The score of the winning board is:", winning_board_score)

    # Solution for 4-b
    print("\n-- Solution for 4-a:")
    losing_board = extract_nth_winning_board(bingo_results, len(boards) - 1)
    losing_board_score = calculate_board_score(
        losing_board.last_draw, losing_board.unmarked_cards
    )
    print("The score of the losing board is:", losing_board_score)
