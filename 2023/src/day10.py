from collections import deque


def read_data(file_name):
    with open(file_name, 'r') as file:
        return [line.strip() for line in file.readlines()]


Position = tuple[int, int]


def find_start_position(grid: list[str]) -> Position:
    for row_index, row in enumerate(grid):
        for col_index, cell in enumerate(row):
            if cell == "S":
                return row_index, col_index

    raise ValueError("No S in this grid")


def find_neighbors(grid: list[str], position: Position, cell: str) -> list[Position]:
    north = tuple(map(sum, zip((-1, 0), position)))
    south = tuple(map(sum, zip((1, 0), position)))
    west = tuple(map(sum, zip((0, -1), position)))
    east = tuple(map(sum, zip((0, 1), position)))
    if cell == "|":
        return [north, south]
    if cell == "-":
        return [west, east]
    if cell == "L":
        return [north, east]
    if cell == "J":
        return [north, west]
    if cell == "7":
        return [south, west]
    if cell == "F":
        return [south, east]
    if cell == ".":
        raise ValueError("Should not search neighbors for a '.' cell")
    if cell == "S":
        # NB: here, I exclude edge case where S is on a border
        neighbors = []
        if grid[north[0]][north[1]] in ["|", "7", "F"]:
            # print("north", north)
            neighbors.append(north)
        if grid[south[0]][south[1]] in ["|", "L", "J"]:
            # print("south", south)
            neighbors.append(south)
        if grid[west[0]][west[1]] in ["-", "L", "F"]:
            # print("west", west)
            neighbors.append(west)
        if grid[east[0]][east[1]] in ["-", "7", "J"]:
            # print("east", east)
            neighbors.append(east)
        return neighbors


def bfs_farthest_point(grid: list[str], start: Position) -> int:
    visited = set()
    to_visit = deque()  # queue
    to_visit.append((start, 0))
    max_depth = 0
    while len(to_visit) > 0:
        position, depth = to_visit.popleft()
        max_depth = max(max_depth, depth)
        visited.add(position)
        cell = grid[position[0]][position[1]]
        neighbors = find_neighbors(grid, position, cell)
        for neighbor in neighbors:
            if neighbor in visited:
                continue
            to_visit.append((neighbor, depth + 1))

    return max_depth


def part_one(grid: list[str]) -> int:
    start = find_start_position(grid)
    return bfs_farthest_point(grid, start)


if __name__ == "__main__":
    # ---- TEST DATA -----
    test_data_1 = [
        ".....",
        ".S-7.",
        ".|.|.",
        ".L-J.",
        "....."
    ]
    test_data_2 = [
        "-L|F7",
        "7S-7|",
        "L|7||",
        "-L-J|",
        "L|-JF"
    ]
    test_data_3 = [
        "..F7.",
        ".FJ|.",
        "SJ.L7",
        "|F--J",
        "LJ..."
    ]
    test_data_4 = [
        "7-F7-",
        ".FJ|7",
        "SJLL7",
        "|F--J",
        "LJ.LJ"
    ]
    print("-- Tests on test data:")
    print(part_one(test_data_1) == 4)
    print(part_one(test_data_2) == 4)
    print(part_one(test_data_3) == 8)
    print(part_one(test_data_4) == 8)
    # print(part_two(test_data) == 2)

    # ---- REAL DATA ----
    data = read_data("./2023/data/day10-input.txt")

    # Solution for part A
    print("\n-- Solution for part A:")
    print(part_one(data))  # 7086
    #
    # # Solution for part B
    # print("\n-- Solution for part B:")
    # print(part_two(data))  # 1066
