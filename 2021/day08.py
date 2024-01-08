#!/usr/bin/env python3
from typing import List, Tuple, Dict, Literal

SignalPattern = str
SignalPatterns = Tuple[SignalPattern, ...]
OutputValue = str
OutputValues = Tuple[OutputValue, ...]
Entry = Tuple[SignalPatterns, OutputValues]
Entries = List[Entry]
Wire = Literal["a", "b", "c", "d", "e", "f", "g"]
Segment = Literal["a", "b", "c", "d", "e", "f", "g"]
SegmentsToWires = Dict[Segment, Wire]
Segments = List[Segment]

SEVEN_SEGMENT_DISPLAY = {
    0: "abcefg",
    1: "cf",
    2: "acdeg",
    3: "acdfg",
    4: "bcdf",
    5: "abdfg",
    6: "abdefg",
    7: "acf",
    8: "abcdefg",
    9: "abcdfg",
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


def count_segments(segments: Segments) -> Dict[Segment, int]:
    segments_count: Dict[Segment, int] = {
        "a": 0,
        "b": 0,
        "c": 0,
        "d": 0,
        "e": 0,
        "f": 0,
        "g": 0,
    }
    for segment in segments:
        segments_count[segment] += 1

    return segments_count


# Seven-segments display used for `map_segments_to_wires` function
#   0:      1:      2:      3:      4:
#  aaaa    ....    aaaa    aaaa    ....
# b    c  .    c  .    c  .    c  b    c
# b    c  .    c  .    c  .    c  b    c
#  ....    ....    dddd    dddd    dddd
# e    f  .    f  e    .  .    f  .    f
# e    f  .    f  e    .  .    f  .    f
#  gggg    ....    gggg    gggg    ....
#
#   5:      6:      7:      8:      9:
#  aaaa    aaaa    aaaa    aaaa    aaaa
# b    .  b    .  .    c  b    c  b    c
# b    .  b    .  .    c  b    c  b    c
#  dddd    dddd    ....    dddd    dddd
# .    f  e    f  .    f  e    f  .    f
# .    f  e    f  .    f  e    f  .    f
#  gggg    gggg    ....    gggg    gggg


def map_segments_to_wires(patterns: SignalPatterns) -> SegmentsToWires:
    # Initialise dictionary
    segment_to_wires: SegmentsToWires = {}

    # Known numbers
    one = next((p for p in patterns if len(p) == 2))
    four = next((p for p in patterns if len(p) == 4))
    seven = next((p for p in patterns if len(p) == 3))

    # Count number of segment repeats among all numbers
    reps = count_segments(list("".join(patterns)))

    # Extract segments
    segment_a: Segment = next(iter(set(seven) - set(one)))
    segment_b: Segment = [s for (s, val) in reps.items() if val == 6][0]
    segment_c: Segment = [s for (s, val) in reps.items() if val == 8 and s in one][0]
    segment_d: Segment = [s for (s, val) in reps.items() if val == 7 and s in four][0]
    segment_e: Segment = [s for (s, val) in reps.items() if val == 4][0]
    segment_f: Segment = [s for (s, val) in reps.items() if val == 9][0]
    segment_g: Segment = [s for (s, val) in reps.items() if val == 7 and s not in four][
        0
    ]

    # Link segments to wires
    segment_to_wires[segment_a]: Wire = "a"
    segment_to_wires[segment_b]: Wire = "b"
    segment_to_wires[segment_c]: Wire = "c"
    segment_to_wires[segment_d]: Wire = "d"
    segment_to_wires[segment_e]: Wire = "e"
    segment_to_wires[segment_f]: Wire = "f"
    segment_to_wires[segment_g]: Wire = "g"

    return segment_to_wires


def decode_value(
    value: OutputValue, segment_to_wires_map: SegmentsToWires
) -> OutputValue:
    decoded_value = ""
    for segment in value:
        decoded_value += segment_to_wires_map[segment]

    return "".join(sorted(decoded_value))


def decode(output_values: OutputValues, segment_to_wires_map: SegmentsToWires) -> int:
    decoded_number = ""
    for value in output_values:
        decoded_value = decode_value(value, segment_to_wires_map)
        decoded_digit = [
            digit
            for (digit, pattern) in SEVEN_SEGMENT_DISPLAY.items()
            if pattern == decoded_value
        ][0]
        decoded_number += str(decoded_digit)

    return int(decoded_number)


if __name__ == "__main__":
    print("-- Tests on test data:")
    # Tests for 8-a
    test_data = read_data("./2021/day08-input-test.txt")
    test_nb_easy_digits = count_nb_easy_digits(test_data)
    print(test_nb_easy_digits == 26)
    # Tests for 8-b
    test_entry: Entry = (
        (
            "acedgfb",
            "cdfbe",
            "gcdfa",
            "fbcad",
            "dab",
            "cefabd",
            "cdfgeb",
            "eafb",
            "cagedb",
            "ab",
        ),
        ("cdfeb", "fcadb", "cdfeb", "cdbaf"),
    )
    test_segment_to_wires_map = map_segments_to_wires(test_entry[0])
    expected_test_segment_to_wires_map = {
        "a": "c",
        "b": "f",
        "c": "g",
        "d": "a",
        "e": "b",
        "f": "d",
        "g": "e",
    }
    print(test_segment_to_wires_map == expected_test_segment_to_wires_map)
    test_decoded_number = decode(test_entry[1], test_segment_to_wires_map)
    print(test_decoded_number == 5353)

    # Solution for 8-a
    print("\n-- Solution for 8-a:")
    entries = read_data("./data/2021/day08-input.txt")
    nb_easy_digits = count_nb_easy_digits(entries)
    print("There are", nb_easy_digits, "easy digits")

    # Solution for 8-b
    print("\n-- Solution for 8-b:")
    total = 0
    for entry in entries:
        segment_to_wires_map = map_segments_to_wires(entry[0])
        decoded_number = decode(entry[1], segment_to_wires_map)
        total += decoded_number
    print("The sum of all decoded numbers is", total)
