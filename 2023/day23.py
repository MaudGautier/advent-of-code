from collections import deque
from copy import copy


def read_data(file_name):
    with open(file_name, 'r') as file:
        return file.read().strip()


Grid = list[list[str]]
Position = tuple[int, int]
ContractedGraph = dict[Position, tuple[Position, int]]


def parse_data(data: str) -> Grid:
    grid = []
    for line in data.splitlines():
        grid.append([])
        for cell in line:
            grid[-1].append(cell)

    return grid


def find_neighbors(grid: Grid, position: Position, visited: set[Position], slopes: bool) -> list[Position]:
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
        if slopes:
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
        neighbors = find_neighbors(grid, position, visited, slopes=True)
        for neighbor in neighbors:
            stack.append((neighbor, depth + 1, copy(visited)))

    return hikes_lengths


def dfs2(start: Position, end: Position, contracted_graph: ContractedGraph):
    stack = deque()
    stack.append((start, 0, set()))
    hikes_lengths = []
    # max_hike = 0
    while len(stack) > 0:
        position, depth, visited = stack.pop()
        if position == end:
            # if depth > max_hike:
            #     max_hike = depth
            #     print("New max", max_hike)
            hikes_lengths.append(depth)
        if position in visited:
            continue
        visited.add(position)
        for neighbor, distance in contracted_graph[position]:
            stack.append((neighbor, depth + distance, copy(visited)))

    return hikes_lengths


def part_one(data: str) -> int:
    grid = parse_data(data)
    start = (0, 1)
    end = (len(grid) - 1, len(grid[0]) - 1 - 1)
    hikes_lengths = dfs(grid, start, end)

    return max(hikes_lengths)


def create_contracted_graph(grid: Grid, start: Position, end: Position) -> ContractedGraph:
    bifurcations = [start, end] + [(i, j) for i in range(len(grid)) for j in range(len(grid[0])) if
                                   len(find_neighbors(grid, (i, j), set(), slopes=False)) >= 3]
    # Always at least 2 bifurcations: itself + other end. We count as bifurcations those that have at least one more
    contracted_graph = {bifurcation: [] for bifurcation in bifurcations}
    for bifurcation in bifurcations:
        for neighbor in find_neighbors(grid, bifurcation, set(), slopes=False):
            current, previous = neighbor, bifurcation
            distance = 1
            while current not in bifurcations:
                current, previous = [node for node in find_neighbors(grid, current, set(), slopes=False) if
                                     node != previous][0], current
                distance += 1
            contracted_graph[bifurcation].append((current, distance))

    return contracted_graph


def part_two(data: str) -> int:
    grid = parse_data(data)
    start = (0, 1)
    end = (len(grid) - 1, len(grid[0]) - 1 - 1)

    contracted_graph = create_contracted_graph(grid, start, end)

    hikes_lengths = dfs2(start, end, contracted_graph=contracted_graph)

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
    print(part_two(test_data) == 154)

    # ---- REAL DATA ----
    data = read_data("./data/2023/day23-input.txt")

    # Solution for part A
    print("\n-- Solution for part A:")
    print(part_one(data))  # 2402
    # Executes in about 1 second

    # Solution for part B
    print("\n-- Solution for part B:")
    print(part_two(data))  # 6450
    # Executes in about 1 minute
