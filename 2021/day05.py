#!/usr/bin/env python3
from typing import List, NamedTuple


class Coord(NamedTuple):
    x: int
    y: int


class VentLine(NamedTuple):
    start: Coord
    end: Coord


VentLines = List[VentLine]
Diagram = List[List[int]]


def read_data(file_name: str) -> VentLines:
    with open(file_name, "r") as file:
        instructions = [instruction.strip() for instruction in file.readlines()]

    vent_lines = []
    for instruction in instructions:
        coordinates = instruction.split(" -> ")
        start_coord = Coord(
            x=int(coordinates[0].split(",")[0]), y=int(coordinates[0].split(",")[1])
        )
        end_coord = Coord(
            x=int(coordinates[1].split(",")[0]), y=int(coordinates[1].split(",")[1])
        )
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
        return range(start, end + 1)

    return range(end, start + 1)


def update_diagram(diagram: Diagram, vent_line: VentLine) -> Diagram:
    # Case horizontal vent lines
    if vent_line.start.x == vent_line.end.x:
        for y_coord in define_range(vent_line.start.y, vent_line.end.y):
            diagram[vent_line.start.x][y_coord] += 1

    # Case vertical vent lines
    if vent_line.start.y == vent_line.end.y:
        for x_coord in define_range(vent_line.start.x, vent_line.end.x):
            diagram[x_coord][vent_line.start.y] += 1

    x_lap = vent_line.end.x - vent_line.start.x
    y_lap = vent_line.end.y - vent_line.start.y

    # Case diagonal vent lines \
    # 1,2
    # 2,3
    # 3,4
    # lapX = 1-3 = -2 (x1-x2)
    # lapY = 2-4 = -2 (y1-y2)
    if x_lap == y_lap:
        # Diagonal is \ (N-W, S-E) => coordinate (start or end) which has min x coord also has min y_coord.
        north_west_coord = Coord(
            x=min(vent_line.start.x, vent_line.end.x),
            y=min(vent_line.start.y, vent_line.end.y),
        )
        for lap in range(abs(x_lap) + 1):
            diagram[north_west_coord.x + lap][north_west_coord.y + lap] += 1

    # Case diagonal vent lines /
    # 0,8
    # 1,7
    # 2,6
    # 3,5
    # 4,4
    # lapX = 0-4 = -4 (x1-x2)
    # lapY = 8-4 = +4 (y1-y2)
    if x_lap == -y_lap:
        # Diagonal is / (N-E, S-W) => coordinate (start or end) which has min x cord also has MAX y coord
        south_west_coord = Coord(
            x=max(vent_line.start.x, vent_line.end.x),
            y=min(vent_line.start.y, vent_line.end.y),
        )
        for lap in range(abs(x_lap) + 1):
            diagram[south_west_coord.x - lap][south_west_coord.y + lap] += 1

    return diagram


def draw_diagram(vent_lines: VentLines, diagram_size: int, diagonals: bool) -> Diagram:
    if not diagonals:
        selected_vent_lines = exclude_diagonal_vent_lines(vent_lines)
    else:
        selected_vent_lines = vent_lines
    diagram = [[0] * (diagram_size + 1) for _ in range(diagram_size + 1)]
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
        max_coord = max(
            vent_line.start.x, vent_line.start.y, vent_line.end.x, vent_line.end.y
        )
        if max_coord > diagram_size:
            diagram_size = max_coord

    return diagram_size


if __name__ == "__main__":
    # Tests
    print("-- Tests on test data:")
    test_vent_lines = read_data("./2021/day05-input-test.txt")
    test_diagram_size = define_diagram_size(test_vent_lines)
    test_diagram = draw_diagram(test_vent_lines, test_diagram_size, diagonals=False)
    test_nb_dangerous_points = count_dangers(test_diagram, 2)
    print(test_nb_dangerous_points == 5)
    test_diagram_with_diags = draw_diagram(test_vent_lines, test_diagram_size, True)
    test_nb_dangerous_points_with_diags = count_dangers(test_diagram_with_diags, 2)
    print(test_nb_dangerous_points_with_diags == 12)

    # Solution for 5-a
    print("-- Solution for 5-a:")
    vent_lines = read_data("./data/2021/day05-input.txt")
    diagram_size = define_diagram_size(vent_lines)
    diagram = draw_diagram(vent_lines, diagram_size, diagonals=False)
    nb_dangerous_points = count_dangers(diagram, 2)
    print("There are", nb_dangerous_points, "dangerous points")

    # Solution for 5-b
    print("-- Solution for 5-b:")
    vent_lines = read_data("./data/2021/day05-input.txt")
    diagram_size = define_diagram_size(vent_lines)
    diagram = draw_diagram(vent_lines, diagram_size, diagonals=True)
    nb_dangerous_points = count_dangers(diagram, 2)
    print("Counting diagonals, there are", nb_dangerous_points, "dangerous points")
