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


def bfs_get_visited(grid: list[str], start: Position) -> set[Position]:
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

    return visited


def count_pipes_north_on_left(position: Position, grid: list[str], pipes) -> int:
    count = 0
    for i in range(0, position[1]):
        # Count J, L and | that correspond to connections to north => know if we are within loop
        # NB: S is because it counts as a "north" (in my dataset + sample data - but should count OR NOT depending on if
        # S connects north/south or east/west)
        if (position[0], i) in pipes and grid[position[0]][i] in ["J", "L", "|", "S"]:
            count += 1
    return count


def part_two(grid: list[str]) -> int:
    start = find_start_position(grid)
    pipes = bfs_get_visited(grid, start)
    nb_tiles = 0
    for row_index, row in enumerate(grid):
        for col_index, cell in enumerate(row):
            if (row_index, col_index) in pipes:
                continue
            nb_north_pipes_left = count_pipes_north_on_left((row_index, col_index), grid, pipes)
            if nb_north_pipes_left % 2 == 1:
                nb_tiles += 1

    return nb_tiles


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
    test_data_5 = [
        "...........",
        ".S-------7.",
        ".|F-----7|.",
        ".||.....||.",
        ".||.....||.",
        ".|L-7.F-J|.",
        ".|..|.|..|.",
        ".L--J.L--J.",
        "..........."
    ]
    test_data_6 = [
        "..........",
        ".S------7.",
        ".|F----7|.",
        ".||OOOO||.",
        ".||OOOO||.",
        ".|L-7F-J|.",
        ".|II||II|.",
        ".L--JL--J.",
        ".........."
    ]
    test_data_7 = [
        ".F----7F7F7F7F-7....",
        ".|F--7||||||||FJ....",
        ".||.FJ||||||||L7....",
        "FJL7L7LJLJ||LJ.L-7..",
        "L--J.L7...LJS7F-7L7.",
        "....F-J..F7FJ|L7L7L7",
        "....L7.F7||L7|.L7L7|",
        ".....|FJLJ|FJ|F7|.LJ",
        "....FJL-7.||.||||...",
        "....L---J.LJ.LJLJ..."
    ]
    test_data_8 = [
        "FF7FSF7F7F7F7F7F---7",
        "L|LJ||||||||||||F--J",
        "FL-7LJLJ||||||LJL-77",
        "F--JF--7||LJLJ7F7FJ-",
        "L---JF-JLJ.||-FJLJJ7",
        "|F|F-JF---7F7-L7L|7|",
        "|FFJF7L7F-JF7|JL---7",
        "7-L-JL7||F7|L7F-7F7|",
        "L.L7LFJ|||||FJL7||LJ",
        "L7JLJL-JLJLJL--JLJ.L"
    ]
    print(part_two(test_data_5) == 4)
    print(part_two(test_data_6) == 4)
    print(part_two(test_data_7) == 8)
    print(part_two(test_data_8) == 10)

    # ---- REAL DATA ----
    data = read_data("./data/2023/day10-input.txt")

    # Solution for part A
    print("\n-- Solution for part A:")
    print(part_one(data))  # 7086

    # Solution for part B
    print("\n-- Solution for part B:")
    print(part_two(data))  # 317
