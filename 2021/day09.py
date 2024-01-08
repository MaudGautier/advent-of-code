#!/usr/bin/env python3
from typing import List, Tuple

HeightMap = List[str]
Point = int
Points = List[Point]
PointCoordinates = Tuple[int, int]
PointsCoordinates = List[Tuple[int, int] or None]
SurroundingPoints = Tuple[Point or None, Point or None, Point or None, Point or None]
BasinSize = int
BasinSizes = List[BasinSize]


def is_a_low_point(point: Point, surrounding_points: SurroundingPoints) -> bool:
    (north, south, east, west) = surrounding_points
    below_north = north is None or point < north
    below_south = south is None or point < south
    below_east = east is None or point < east
    below_west = west is None or point < west
    return below_north and below_west and below_east and below_south


def find_low_points_coordinates(height_map: HeightMap) -> PointsCoordinates:
    nb_rows = len(height_map)
    nb_cols = len(height_map[0])
    low_points_coordinates: PointsCoordinates = []
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
                low_points_coordinates.append((row_index, col_index))

    return low_points_coordinates


def get_point_values(
    height_map: HeightMap, point_coordinates: PointsCoordinates
) -> Points:
    points: Points = []
    for (row_index, col_index) in point_coordinates:
        points.append(int(height_map[row_index][col_index]))

    return points


def compute_total_risk_level(low_points: Points) -> int:
    return sum(low_points) + len(low_points)


def read_data(file_name: str) -> HeightMap:
    with open(file_name, "r") as file:
        return [line[:-1] for line in file.readlines()]


def extract_coords_to_append(
    height_map: HeightMap, x: int, y: int, nb_rows: int, nb_cols: int
) -> PointsCoordinates:
    north_coord = (x - 1, y) if x != 0 else None
    south_coord = (x + 1, y) if x != nb_rows - 1 else None
    west_coord = (x, y - 1) if y != 0 else None
    east_coord = (x, y + 1) if y != nb_cols - 1 else None
    coords_to_append = []
    if north_coord is not None and int(height_map[north_coord[0]][north_coord[1]]) < 9:
        coords_to_append.append(north_coord)
    if south_coord is not None and int(height_map[south_coord[0]][south_coord[1]]) < 9:
        coords_to_append.append(south_coord)
    if east_coord is not None and int(height_map[east_coord[0]][east_coord[1]]) < 9:
        coords_to_append.append(east_coord)
    if west_coord is not None and int(height_map[west_coord[0]][west_coord[1]]) < 9:
        coords_to_append.append(west_coord)
    return coords_to_append


def define_basin_points(
    height_map: HeightMap, point_coord: PointCoordinates
) -> PointsCoordinates:
    nb_rows = len(height_map)
    nb_cols = len(height_map[0])
    basin_point_coordinates = [point_coord]
    basin_frontiers = [point_coord]
    while len(basin_frontiers) > 0:
        new_basin_frontiers = []
        for (x, y) in basin_frontiers:
            coords_to_append = extract_coords_to_append(
                height_map=height_map, x=x, y=y, nb_rows=nb_rows, nb_cols=nb_cols
            )
            for coord in coords_to_append:
                if coord not in basin_point_coordinates:
                    basin_point_coordinates.append(coord)
                    new_basin_frontiers.append(coord)
        basin_frontiers = new_basin_frontiers

    return basin_point_coordinates


def find_basin_sizes(height_map: HeightMap) -> BasinSizes:
    low_points_coordinates = find_low_points_coordinates(height_map)
    basin_sizes: BasinSizes = []
    for point_coord in low_points_coordinates:
        basin_points = define_basin_points(height_map, point_coord)
        basin_sizes.append(len(basin_points))
    return basin_sizes


def multiply_three_largest(sizes: BasinSizes) -> int:
    three_largest = sorted(sizes)[-3:]
    return three_largest[0] * three_largest[1] * three_largest[2]


if __name__ == "__main__":
    print("-- Tests on test data:")
    test_data: HeightMap = [
        "2199943210",
        "3987894921",
        "9856789892",
        "8767896789",
        "9899965678",
    ]
    # Test part a
    test_low_points_coordinates = find_low_points_coordinates(test_data)
    test_low_points = get_point_values(test_data, test_low_points_coordinates)
    print(test_low_points == [1, 0, 5, 5])
    test_total_risk_level = compute_total_risk_level(test_low_points)
    print(test_total_risk_level == 15)
    # Test part b
    test_basin_sizes = find_basin_sizes(test_data)
    print(test_basin_sizes == [3, 9, 14, 9])
    test_three_largest_multiplication = multiply_three_largest(test_basin_sizes)
    print(test_three_largest_multiplication == 1134)

    # Solution for 9-a
    print("\n-- Solution for 9-a:")
    height_map = read_data("./data/2021/day09-input.txt")
    low_points_coordinates = find_low_points_coordinates(height_map)
    low_points = get_point_values(height_map, low_points_coordinates)
    total_risk_level = compute_total_risk_level(low_points)
    print("The total risk level is", total_risk_level)

    # Solution for 9-b
    print("\n-- Solution for 9-b:")
    basin_sizes = find_basin_sizes(height_map)
    three_largest_multiplication = multiply_three_largest(basin_sizes)
    print(
        "The product of the three largest basin sizes is", three_largest_multiplication
    )
