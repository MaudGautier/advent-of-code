#!/usr/bin/env python3
from typing import List, Tuple, NamedTuple

class Coord(NamedTuple):
    x: int
    y: int

class VentLine(NamedTuple):
    start: Coord
    end: Coord

VentLines = List[VentLine]
Diagram = List[List[int]]


def read_data(file_name: str) -> VentLines:
    with open(file_name, 'r') as file:
        instructions = [instruction.strip() for instruction in file.readlines()]
    print(instructions)

    vent_lines = []

    for instruction in instructions:
        coordinates = instruction.split(' -> ')
        start_coord = Coord(int(coordinates[0].split(",")[0]), int(coordinates[0].split(",")[1]))
        end_coord = Coord(int(coordinates[1].split(",")[0]), int(coordinates[1].split(",")[1]))
        vent_line = VentLine(start=start_coord, end=end_coord)
        vent_lines.append(vent_line)

    return vent_lines


def exclude_diagonal_vent_lines(vent_lines: VentLines) -> VentLines:
    selected_vent_lines = []
    for vent_line in vent_lines:
        if vent_line.start.x == vent_line.end.x or vent_line.start.y == vent_line.end.y:
            selected_vent_lines.append(vent_line)

    return selected_vent_lines


def define_range(start: int, end: int) -> range:
    if start < end:
        return range(start, end+1)

    return range(end, start+1)


def update_diagram(diagram: Diagram, vent_line: VentLine) -> Diagram:
    # Case horizontal vent lines
    if vent_line.start.x == vent_line.end.x:
        for y_coord in define_range(vent_line.start.y, vent_line.end.y):
            diagram[vent_line.start.x][y_coord] += 1

    # Case vertical vent lines
    if vent_line.start.y == vent_line.end.y:
        for x_coord in define_range(vent_line.start.x, vent_line.end.x):
            diagram[x_coord][vent_line.start.y] += 1

    return diagram


def draw_diagram(vent_lines: VentLines, diagram_size: int) -> Diagram:
    selected_vent_lines = exclude_diagonal_vent_lines(vent_lines)
    diagram = [[0]*(diagram_size+1) for row in range(diagram_size + 1)]
    for selected_vent_line in selected_vent_lines:
        diagram = update_diagram(diagram, selected_vent_line)

    return diagram


def count_dangers(diagram: Diagram, danger_threshold: int) -> int:
    counter = 0
    for index_row, row in enumerate(diagram):
        for index_column, column in enumerate(row):
            if diagram[index_row][index_column] >= danger_threshold:
                counter += 1

    return counter


def define_diagram_size(vent_lines: VentLines) -> int:
    diagram_size = 0
    for vent_line in vent_lines:
        max_coord = max(vent_line.start.x, vent_line.start.y, vent_line.end.x, vent_line.end.y)
        if max_coord > diagram_size:
            diagram_size = max_coord

    return diagram_size


if __name__ == '__main__':
    # Tests
    print("-- Tests on test data:")
    test_vent_lines = read_data('data/day05-input-test.txt')
    test_diagram = draw_diagram(test_vent_lines, 9)
    test_nb_dangerous_points = count_dangers(test_diagram, 2)
    print(test_nb_dangerous_points == 5)

    # Solution for 5-a
    print("-- Solution for 5-a:")
    vent_lines = read_data('data/day05-input.txt')
    diagram_size = define_diagram_size(vent_lines)
    diagram = draw_diagram(vent_lines, diagram_size)
    nb_dangerous_points = count_dangers(diagram, 2)
    print("There are", nb_dangerous_points, "dangerous points")


