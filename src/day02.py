#!/usr/bin/env python3
from typing import Tuple, List


def format_instructions(path: str) -> List[Tuple[str, int]]:
    with open(path, 'r') as file:
        lines = [line.strip().split(" ") for line in file.readlines()]
        return [(str(x), int(y)) for [x, y] in lines]


def update_coord(coord: Tuple[int, int], instruction: Tuple[str, int]) -> Tuple[int, int]:
    [direction, value] = instruction
    horizontal_position = coord[0]
    depth = coord[1]

    if direction == 'forward':
        horizontal_position += value
    elif direction == 'down':
        depth += value
    elif direction == 'up':
        depth -= value

    return horizontal_position, depth


def calculate_final_coordinates(instructions: List[Tuple[str, int]], initial_coord: Tuple[int, int]) -> Tuple[int, int]:
    current_coord = initial_coord
    for instruction in instructions:
        current_coord = update_coord(current_coord, instruction)
    return current_coord


def multiply_coordinates(coordinates: Tuple[int, int]) -> int:
    return coordinates[0] * coordinates[1]


if __name__ == "__main__":
    file_path = 'data/day02-input.txt'
    instructions = format_instructions(file_path)
    # Manual check
    instructions_subset = instructions[0:5]
    print("## for instructions:", instructions_subset, ", the final coordinates are:", calculate_final_coordinates(instructions_subset, (0, 0)))
    final_coordinates = calculate_final_coordinates(instructions, (0, 0))
    coordinates_multiplier = multiply_coordinates(final_coordinates)
    # Final solution
    print("## For full list of instructions, the final coordinates are:", final_coordinates, "and the multiplier is:", coordinates_multiplier)

