#!/usr/bin/env python3
from typing import List, Callable, Optional, NamedTuple

Coordinates = NamedTuple(
    "Coordinates",
    (("horizontal_position", int), ("depth", int), ("aim", Optional[int])),
)

Instruction = NamedTuple("Instruction", (("direction", str), ("value", int)))


def format_instructions(path: str) -> List[Instruction]:
    with open(path, "r") as file:
        lines = [line.strip().split(" ") for line in file.readlines()]
        return [(str(x), int(y)) for [x, y] in lines]


def update_coord_v1(coord: Coordinates, instruction: Instruction) -> Coordinates:
    [direction, value] = instruction
    horizontal_position = coord.horizontal_position
    depth = coord.depth

    if direction == "forward":
        horizontal_position += value
    elif direction == "down":
        depth += value
    elif direction == "up":
        depth -= value

    return Coordinates(horizontal_position, depth, None)


def update_coord_v2(coord: Coordinates, instruction: Instruction) -> Coordinates:
    [direction, value] = instruction
    [horizontal_position, depth, aim] = coord

    if direction == "forward":
        horizontal_position += value
        depth += aim * value
    elif direction == "down":
        aim += value
    elif direction == "up":
        aim -= value

    return Coordinates(horizontal_position, depth, aim)


def calculate_final_coordinates(
    instructions: List[Instruction],
    initial_coord: Coordinates,
    update_coordinates_function: Callable[[Coordinates, Instruction], Coordinates],
) -> Coordinates:
    current_coord = initial_coord
    for instruction in instructions:
        current_coord = update_coordinates_function(current_coord, instruction)
    return current_coord


def multiply_coordinates(coordinates: Coordinates) -> int:
    return coordinates.horizontal_position * coordinates.depth


if __name__ == "__main__":
    file_path = "data/day02-input.txt"
    instructions = format_instructions(file_path)
    initial_coord_v1 = Coordinates(0, 0, None)
    initial_coord_v2 = Coordinates(0, 0, 0)

    # Manual check
    instructions_check_data = [
        ("forward", 5),
        ("down", 5),
        ("forward", 8),
        ("up", 3),
        ("down", 8),
        ("forward", 2),
    ]
    check_data_coordinates_v1 = calculate_final_coordinates(
        instructions_check_data, initial_coord_v1, update_coord_v1
    )
    check_data_coordinates_v2 = calculate_final_coordinates(
        instructions_check_data, initial_coord_v2, update_coord_v2
    )
    print(check_data_coordinates_v1[0:2] == (15, 10))
    print(check_data_coordinates_v2[0:2] == (15, 60))

    # Final solution v1
    final_coordinates = calculate_final_coordinates(
        instructions, initial_coord_v1, update_coord_v1
    )
    coordinates_multiplier = multiply_coordinates(final_coordinates)
    print(
        "## For full list of instructions, the final coordinates are:",
        final_coordinates,
        "and the multiplier is:",
        coordinates_multiplier,
    )

    # Final solution v2
    final_coordinates = calculate_final_coordinates(
        instructions, initial_coord_v2, update_coord_v2
    )
    coordinates_multiplier = multiply_coordinates(final_coordinates)
    print(
        "## For full list of instructions, the final coordinates are:",
        final_coordinates,
        "and the multiplier is:",
        coordinates_multiplier,
    )
