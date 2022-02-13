#!/usr/bin/env python3
from typing import List, Tuple

HeightMap = List[str]
Point = int
Points = List[Point]
SurroundingPoints = Tuple[Point or None, Point or None, Point or None, Point or None]


def is_a_low_point(point: Point, surrounding_points: SurroundingPoints) -> bool:
    (north, south, east, west) = surrounding_points
    below_north = north is None or point < north
    below_south = south is None or point < south
    below_east = east is None or point < east
    below_west = west is None or point < west
    return below_north and below_west and below_east and below_south


def find_low_points(height_map: HeightMap) -> Points:
    nb_rows = len(height_map)
    nb_cols = len(height_map[0])
    low_points: Points = []
    for row_index, row in enumerate(height_map):
        for col_index, cell in enumerate(row):
            north = height_map[row_index - 1][col_index] if row_index != 0 else None
            south = (
                height_map[row_index + 1][col_index]
                if row_index != nb_rows - 1
                else None
            )
            west = height_map[row_index][col_index - 1] if col_index != 0 else None
            east = (
                height_map[row_index][col_index + 1]
                if col_index != nb_cols - 1
                else None
            )
            if is_a_low_point(cell, (north, south, east, west)):
                low_points.append(int(cell))

    return low_points


def compute_total_risk_level(low_points: Points) -> int:
    return sum(low_points) + len(low_points)


def read_data(file_name: str) -> HeightMap:
    with open(file_name, "r") as file:
        return [line[:-1] for line in file.readlines()]


if __name__ == "__main__":
    print("-- Tests on test data:")
    test_data: HeightMap = [
        "2199943210",
        "3987894921",
        "9856789892",
        "8767896789",
        "9899965678",
    ]
    test_low_points = find_low_points(test_data)
    print(test_low_points == [1, 0, 5, 5])
    test_total_risk_level = compute_total_risk_level(test_low_points)
    print(test_total_risk_level == 15)

    # Solution for 9-a
    print("\n-- Solution for 9-a:")
    height_map = read_data("data/day09-input.txt")
    print(height_map)
    low_points = find_low_points(height_map)
    total_risk_level = compute_total_risk_level(low_points)
    print("The total risk level is", total_risk_level)
