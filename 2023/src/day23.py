from collections import deque
from copy import copy


def read_data(file_name):
    with open(file_name, 'r') as file:
        return file.read().strip()


Grid = list[list[str]]
Position = tuple[int, int]


def parse_data(data: str) -> Grid:
    grid = []
    for line in data.splitlines():
        grid.append([])
        for cell in line:
            grid[-1].append(cell)

    return grid


def find_neighbors(grid: Grid, position: Position, visited: set[Position]) -> list[Position]:
    offsets = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    neighbors = []
    for dx, dy in offsets:
        x, y = position[0] + dx, position[1] + dy

        # Do not get outside of grid
        if not (0 <= x < len(grid) and 0 <= y < len(grid[0])):
            continue

        # Do not walk on rock
        if grid[x][y] == "#":
            continue

        # Do not revisit cell already visited
        if (x, y) in visited:
            continue

        # Prevent going on slopes in the incorrect direction
        if grid[x][y] == ">" and (dx, dy) != (0, 1):
            continue
        if grid[x][y] == "<" and (dx, dy) != (0, -1):
            continue
        if grid[x][y] == "v" and (dx, dy) != (1, 0):
            continue
        if grid[x][y] == "^" and (dx, dy) != (-1, 0):
            continue

        neighbors.append((x, y))

    return neighbors


def dfs(grid: Grid, start: Position, end: Position):
    stack = deque()
    stack.append((start, 0, set()))
    hikes_lengths = []
    while len(stack) > 0:
        position, depth, visited = stack.pop()
        if position == end:
            hikes_lengths.append(depth)
        if position in visited:
            continue
        visited.add(position)
        neighbors = find_neighbors(grid, position, visited)
        for neighbor in neighbors:
            stack.append((neighbor, depth + 1, copy(visited)))

    return hikes_lengths


def part_one(data: str) -> int:
    grid = parse_data(data)
    start = (0, 1)
    end = (len(grid) - 1, len(grid[0]) - 1 - 1)
    hikes_lengths = dfs(grid, start, end)

    return max(hikes_lengths)


if __name__ == "__main__":
    # ---- TEST DATA -----
    test_data = r"""#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#"""
    print("-- Tests on test data:")
    print(part_one(test_data) == 94)
    # print(part_two(test_data) == 7)

    # ---- REAL DATA ----
    data = read_data("./2023/data/day23-input.txt")

    # Solution for part A
    print("\n-- Solution for part A:")
    print(part_one(data))  # 2402
    # Executes in about 1 second
    #
    # # Solution for part B
    # print("\n-- Solution for part B:")
    # print(part_two(data))  # 61297
