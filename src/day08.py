#!/usr/bin/env python3
from typing import List, Tuple

SignalPattern = str
SignalPatterns = Tuple[str]
OutputValue = str
OutputValues = Tuple[OutputValue]
Entry = Tuple[SignalPatterns, OutputValues]
Entries = List[Entry]

SEVEN_SEGMENT_DISPLAY = {
    1: "cf",
    4: "bcdf",
    7: "acf",
    8: "abcdefg",
}
EASY_DIGITS = [1, 4, 7, 8]  # Digits with a unique number of segments


def read_data(file_name: str) -> Entries:
    entries = []
    with open(file_name, "r") as file:
        lines = file.readlines()
        for line in lines:
            signal_patterns = tuple(line.strip().split(" | ")[0].split(" "))
            output_values = tuple(line.strip().split(" | ")[1].split(" "))
            entries.append((signal_patterns, output_values))

    return entries


def count_nb_easy_digits(entries: Entries) -> int:
    easy_digit_segment_lengths = [
        len(SEVEN_SEGMENT_DISPLAY[key]) for key in EASY_DIGITS
    ]
    counter = 0
    for _, output_values in entries:
        for value in output_values:
            if len(value) in easy_digit_segment_lengths:
                counter += 1

    return counter


if __name__ == "__main__":
    # Tests
    print("-- Tests on test data:")
    test_data = read_data("data/day08-input-test.txt")
    test_nb_easy_digits = count_nb_easy_digits(test_data)
    print(test_nb_easy_digits == 26)

    # Solution for 8-a
    print("\n-- Solution for 8-a:")
    entries = read_data("data/day08-input.txt")
    nb_easy_digits = count_nb_easy_digits(entries)
    print("There are", nb_easy_digits, "easy digits")
