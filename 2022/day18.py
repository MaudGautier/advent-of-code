import math
import sys

print(sys.getrecursionlimit())

sys.setrecursionlimit(10000)


def read_data(file_name):
    with open(file_name, 'r') as file:
        lines = [line.split(",") for line in file.readlines()]
        return [(int(x), int(y), int(z)) for [x, y, z] in lines]


def compute_number_sides_touching(coordinates):
    number_sides_touching = 0
    for x1, y1, z1 in coordinates:
        for x2, y2, z2 in coordinates:
            # Touching on z
            if x1 == x2 and y1 == y2 and abs(z1 - z2) == 1:
                number_sides_touching += 1
            # Touching on y
            if x1 == x2 and abs(y1 - y2) == 1 and z1 == z2:
                number_sides_touching += 1
            # Touching on x
            if abs(x1 - x2) == 1 and y1 == y2 and z1 == z2:
                number_sides_touching += 1

    return number_sides_touching


def part_one(coordinates):
    number_sides_touching = compute_number_sides_touching(coordinates)
    total_number_sides = len(coordinates) * 6

    return total_number_sides - number_sides_touching


def compute_ranges(coordinates):
    min_x, min_y, min_z = math.inf, math.inf, math.inf
    max_x, max_y, max_z = 0, 0, 0
    for x, y, z in coordinates:
        max_x = max(max_x, x)
        max_y = max(max_y, y)
        max_z = max(max_z, z)
        min_x = min(min_x, x)
        min_y = min(min_y, y)
        min_z = min(min_z, z)
    return (min_x - 1, max_x + 1), (min_y - 1, max_y + 1), (min_z - 1, max_z + 1)


def compute_number_cubes_trapped(coordinates):
    ((min_x, max_x), (min_y, max_y), (min_z, max_z)) = compute_ranges(coordinates)
    # print((min_x, max_x), (min_y, max_y), (min_z, max_z))

    number_trapped = 0
    list_trapped = []
    set_coordinates = set(coordinates)
    for x in range(min_x, max_x):
        for y in range(min_y, max_y):
            for z in range(min_z, max_z):
                if (x, y, z) not in set_coordinates and \
                        (x + 1, y, z) in set_coordinates and (x - 1, y, z) in set_coordinates and \
                        (x, y + 1, z) in set_coordinates and (x, y - 1, z) in set_coordinates and \
                        (x, y, z + 1) in set_coordinates and (x, y, z - 1) in set_coordinates:
                    number_trapped += 1
                    list_trapped.append((x, y, z))
    print(list_trapped)
    return number_trapped


# Algo = je pars d'un point externe puis je construis la map de tous ceux qui sont dehors
# def compute_number_coords_inside(coordinates):
#     ((min_x, max_x), (min_y, max_y), (min_z, max_z)) = compute_ranges(coordinates)
#     set_coordinates = set(coordinates)
#
#     if (min_x, min_y, min_z) in set_coordinates:
#         print("PROBLEM: START POINT IN COORDINATES !! ")
#
#     set_outsides = set()
#     set_outsides.add((min_x, min_y, min_z))
#     for x in range(min_x, max_x):
#         for y in range(min_y, max_y):
#             for z in range(min_z, max_z):
#                 if (x, y, z) == (2, 2, 4):
#                     print(set_outsides)
#                     print((x, y, z) not in set_coordinates,
#                           (x + 1, y, z) in set_outsides, (x - 1, y, z) in set_outsides,
#                           (x, y + 1, z) in set_outsides, (x, y - 1, z) in set_outsides,
#                           (x, y, z + 1) in set_outsides, (x, y, z - 1) in set_outsides)
#                 if (x, y, z) not in set_coordinates and \
#                         ((x + 1, y, z) in set_outsides or (x - 1, y, z) in set_outsides or \
#                          (x, y + 1, z) in set_outsides or (x, y - 1, z) in set_outsides or \
#                          (x, y, z + 1) in set_outsides or (x, y, z - 1) in set_outsides):
#                     set_outsides.add((x, y, z))
#
#     number_trapped = 0
#     set_trapped = set()
#     for x in range(min_x, max_x):
#         for y in range(min_y, max_y):
#             for z in range(min_z, max_z):
#                 if (x, y, z) not in set_coordinates and (x, y, z) not in set_outsides:
#                     set_trapped.add((x, y, z))
#                     number_trapped += 1
#
#     print("RES", number_trapped, set_trapped)
#
#     print(set_outsides)
#     print(len(set_outsides))
#     print((max_x - min_x) * (max_y - min_y) * (max_z - min_z))
#     total_number = (max_x - min_x) * (max_y - min_y) * (max_z - min_z)
#     return total_number - len(set_outsides)

def compute_neighbors(current_coordinates, ranges, already_visited):
    ((min_x, max_x), (min_y, max_y), (min_z, max_z)) = ranges
    x, y, z = current_coordinates
    candidate_neighbors = [(x + 1, y, z), (x - 1, y, z), (x, y + 1, z), (x, y - 1, z), (x, y, z + 1), (x, y, z - 1)]
    neighbors = []
    for xn, yn, zn in candidate_neighbors:
        if not (min_x <= xn <= max_x and min_y <= yn <= max_y and min_z <= zn <= max_z):
            continue
        if (xn, yn, zn) in already_visited:
            continue
        neighbors.append((xn, yn, zn))
    return neighbors


# Algo:
# Pars d'un point outside
# Calcule ses 8 voisins
# Si voisin pas dans set_coord => ajoute à la liste des outside et regarde ses voisins à lui
# Si voisin dans liste des coord => STOP
def dfs(current_coordinates, ranges, already_visited, coordinates_cubes, list_drops_outside):
    # ((min_x, max_x), (min_y, max_y), (min_z, max_z)) = ranges
    x, y, z = current_coordinates
    neighbors = compute_neighbors(current_coordinates, ranges, already_visited)

    # Stop condition: current_node in list des coordinates
    if (x, y, z) in coordinates_cubes:
        already_visited.append(current_coordinates)
        return

    # Else: Add node to list
    already_visited.append(current_coordinates)
    list_drops_outside.append(current_coordinates)

    for neighbor in neighbors:
        dfs(current_coordinates=neighbor,
            ranges=ranges,
            already_visited=already_visited,
            coordinates_cubes=coordinates_cubes,
            list_drops_outside=list_drops_outside)

    # # Stop condition (outside of range)
    # if x < min_x or y < min_y or z < min_z or x >= max_x or y >= max_y or z >= max_z:
    #     # list_drops_outside.append((x, y, z))
    #     return (x, y, z)
    #
    # list_neighbors = [(x+1, y, z), (x-1, y, z), (x, y+1, z), (x, y-1, z), (x, y, z+1), (x, y, z-1)]
    # for neighbor in list_neighbors:
    #
    #


def part_two(coordinates):
    number_sides_touching = compute_number_sides_touching(coordinates)
    total_number_sides = len(coordinates) * 6
    # number_cubes_trapped_in_droplets = compute_number_cubes_trapped(coordinates)

    ranges = compute_ranges(coordinates)
    ((min_x, max_x), (min_y, max_y), (min_z, max_z)) = ranges
    already_visited = []
    start_point = (min_x, min_y, min_z)
    if start_point in coordinates:
        print("PROBLEM START POINT")
    list_drops_outside = []
    dfs(current_coordinates=start_point,
        ranges=ranges,
        already_visited=already_visited,
        coordinates_cubes=coordinates,
        list_drops_outside=list_drops_outside)
    print(list_drops_outside, len(set(list_drops_outside)))
    total_number_drops_in_cube = (max_x - min_x + 1) * (max_y - min_y + 1) * (max_z - min_z + 1)
    print("len(set(list_drops_outside))", len(set(list_drops_outside)))
    print("total_number_drops_in_cube", total_number_drops_in_cube)
    number_drops_inside = total_number_drops_in_cube - len(set(list_drops_outside))
    print("number_drops_inside", number_drops_inside)
    number_cubes_trapped = number_drops_inside - len(coordinates)
    # cubes_trapped = []
    all_points_in_cube = []
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            for z in range(min_z, max_z + 1):
                all_points_in_cube.append((x, y, z))
    print('-- all_points_in_cube', all_points_in_cube, len(all_points_in_cube), len(set(all_points_in_cube)))
    set_all_points_in_cube = set(all_points_in_cube)
    set_drops_outside = set(list_drops_outside)
    set_drops_inside = set_all_points_in_cube - set_drops_outside
    print("-- set_drops_inside", set_drops_inside, len(set_drops_inside))
    set_coordinates = set(coordinates)
    set_trapped = set_drops_inside - set_coordinates
    print("-- set_trapped", set_trapped, len(set_trapped))

    print("number_cubes_trapped", number_cubes_trapped)
    print("total_number_sides", total_number_sides)
    print("number_sides_touching", number_sides_touching)
    print("number_cubes_trapped * 6", number_cubes_trapped * 6)

    surface_trapped = part_one(list(set_trapped))
    print("surface_trapped", surface_trapped)

    return total_number_sides - number_sides_touching - surface_trapped
    #
    # number_coords_inside = compute_number_coords_inside(coordinates)
    # print(number_coords_inside)
    # print(number_coords_inside)
    # # print(number_coords_inside * 6 - number_sides_touching)
    # return total_number_sides - number_sides_touching - number_cubes_trapped_in_droplets * 6


if __name__ == "__main__":
    # ---- TEST DATA -----
    test_data = [
        (2, 2, 2),
        (1, 2, 2),
        (3, 2, 2),
        (2, 1, 2),
        (2, 3, 2),
        (2, 2, 1),
        (2, 2, 3),
        (2, 2, 4),
        (2, 2, 6),
        (1, 2, 5),
        (3, 2, 5),
        (2, 1, 5),
        (2, 3, 5)
    ]
    print("-- Tests on test data:")
    # print(part_one(test_data) == 64)
    print(part_two(test_data) == 58)  # 58 with real case

    test_data = [
        (0, 1, 1),
        (1, 0, 1),
        (1, 1, 0),
        # z = 1
        (1, 1, 1),
        (1, 2, 1),
        (1, 3, 1),
        (1, 4, 1),
        (1, 5, 1),
        (2, 1, 1),
        (2, 2, 1),
        (2, 3, 1),
        (2, 4, 1),
        (2, 5, 1),
        (3, 1, 1),
        (3, 2, 1),
        (3, 3, 1),
        (3, 4, 1),
        (3, 5, 1),
        (4, 1, 1),
        (4, 2, 1),
        (4, 3, 1),
        (4, 4, 1),
        (4, 5, 1),
        (5, 1, 1),
        (5, 2, 1),
        (5, 3, 1),
        (5, 4, 1),
        (5, 5, 1),
        # z = 2
        (1, 1, 2),
        (1, 2, 2),
        (1, 3, 2),
        (1, 4, 2),
        (1, 5, 2),
        (2, 1, 2),
        (2, 2, 2),
        (2, 3, 2),
        (2, 4, 2),
        (2, 5, 2),
        (3, 1, 2),
        (3, 2, 2),
        (3, 3, 2),
        (3, 4, 2),
        (3, 5, 2),
        (4, 1, 2),
        (4, 2, 2),
        (4, 3, 2),
        (4, 4, 2),
        (4, 5, 2),
        (5, 1, 2),
        (5, 2, 2),
        (5, 3, 2),
        (5, 4, 2),
        (5, 5, 2),
        # z = 3
        (1, 1, 3),
        (1, 2, 3),
        (1, 3, 3),
        (1, 4, 3),
        (1, 5, 3),
        (2, 1, 3),
        (2, 2, 3),
        (2, 3, 3),
        (2, 4, 3),
        (2, 5, 3),
        (3, 1, 3),
        # (3, 2, 3),
        # (3, 3, 3),
        # (3, 4, 3),
        (3, 5, 3),
        (4, 1, 3),
        (4, 2, 3),
        (4, 3, 3),
        (4, 4, 3),
        (4, 5, 3),
        (5, 1, 3),
        (5, 2, 3),
        (5, 3, 3),
        (5, 4, 3),
        (5, 5, 3),
        # z = 4
        (1, 1, 4),
        (1, 2, 4),
        (1, 3, 4),
        (1, 4, 4),
        (1, 5, 4),
        (2, 1, 4),
        (2, 2, 4),
        (2, 3, 4),
        (2, 4, 4),
        (2, 5, 4),
        (3, 1, 4),
        (3, 2, 4),
        # (3, 3, 4),
        (3, 4, 4),
        (3, 5, 4),
        (4, 1, 4),
        (4, 2, 4),
        (4, 3, 4),
        (4, 4, 4),
        (4, 5, 4),
        (5, 1, 4),
        (5, 2, 4),
        (5, 3, 4),
        # (5, 4, 4),
        (5, 5, 4),
        # z = 5
        (1, 1, 5),
        (1, 2, 5),
        (1, 3, 5),
        (1, 4, 5),
        (1, 5, 5),
        (2, 1, 5),
        (2, 2, 5),
        (2, 3, 5),
        (2, 4, 5),
        (2, 5, 5),
        (3, 1, 5),
        (3, 2, 5),
        (3, 3, 5),
        (3, 4, 5),
        (3, 5, 5),
        (4, 1, 5),
        (4, 2, 5),
        (4, 3, 5),
        (4, 4, 5),
        (4, 5, 5),
        (5, 1, 5),
        (5, 2, 5),
        (5, 3, 5),
        (5, 4, 5),
        (5, 5, 5),
    ]
    print(part_two(test_data))  # 58 with real case

    # # # ---- REAL DATA ----
    data = read_data("./data/2022/day18-input.txt")
    # #
    # # # Solution for part A
    # # print("\n-- Solution for part A:")
    # # print(part_one(data))  # 3526
    # # #
    # # # Solution for part B
    # print("\n-- Solution for part B:")
    print(part_two(data))  # 3316 INCORRECT TOO HIGH # 2072 TOO LOW # Correct = 2090 surface (1060 trapped)
