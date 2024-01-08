from collections import deque


def read_data(file_name):
    with open(file_name, 'r') as file:
        return file.read().strip()


Grid = list[list[str]]
Position = tuple[int, int]


def parse_data(data: str) -> Grid:
    rows = data.split("\n")
    grid = []
    for i, row in enumerate(rows):
        grid.append([])
        for cell in row:
            grid[i].append(cell)
    return grid


def find_start(grid: Grid) -> Position:
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == "S":
                return i, j

    raise ValueError("No start position in this grid! This should not happen.")


def find_neighbors(grid: Grid, position: Position) -> list[Position]:
    size = len(grid)
    offsets = [(0, 1), (0, -1), (-1, 0), (1, 0)]
    neighbors = []
    for offset in offsets:
        x = position[0] + offset[0]
        y = position[1] + offset[1]
        if grid[x % size][y % size] == "#":
            continue
        neighbors.append((x, y))
    return neighbors


def walk(grid: Grid, nb_steps: int) -> int:
    start = find_start(grid)

    queue = deque()
    queue.append([start])

    for step in range(nb_steps):
        currents = queue.popleft()
        all_neighbors = set()
        for current in currents:
            neighbors = find_neighbors(grid, current)
            for neighbor in neighbors:
                all_neighbors.add(neighbor)

        queue.append(all_neighbors)

    currents_last_step = queue.popleft()
    return len(currents_last_step)


def part_one(data: str, nb_steps: int) -> int:
    grid = parse_data(data)

    return walk(grid, nb_steps)


def part_two(data: str, nb_steps: int) -> int:
    grid = parse_data(data)
    size = len(grid)
    half_grid = size // 2

    # Data points to get to half grid + 0, 1 or 2 grids
    x_1 = 0  # half_grid
    x_2 = 1  # half_grid + size
    x_3 = 2  # half_grid + 2 * size
    y_1 = walk(grid, half_grid)
    y_2 = walk(grid, half_grid + size)
    y_3 = walk(grid, half_grid + 2 * size)

    # Get coefficients via Lagrange interpolation
    # (https://stackoverflow.com/questions/16896577/using-points-to-generate-quadratic-equation-to-interpolate-data)
    a = y_1 / ((x_1 - x_2) * (x_1 - x_3)) + y_2 / ((x_2 - x_1) * (x_2 - x_3)) + y_3 / ((x_3 - x_1) * (x_3 - x_2))

    b = (-y_1 * (x_2 + x_3) / ((x_1 - x_2) * (x_1 - x_3))
         - y_2 * (x_1 + x_3) / ((x_2 - x_1) * (x_2 - x_3))
         - y_3 * (x_1 + x_2) / ((x_3 - x_1) * (x_3 - x_2)))

    c = (y_1 * x_2 * x_3 / ((x_1 - x_2) * (x_1 - x_3))
         + y_2 * x_1 * x_3 / ((x_2 - x_1) * (x_2 - x_3))
         + y_3 * x_1 * x_2 / ((x_3 - x_1) * (x_3 - x_2)))

    # Use coefficients to compute the result
    m = (nb_steps - half_grid) // size
    # m = 202300
    return int(a * m * m + b * m + c)


if __name__ == "__main__":
    # ---- TEST DATA -----
    test_data = r"""...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
..........."""
    print("-- Tests on test data:")
    print(part_one(test_data, 6) == 16)

    # ---- REAL DATA ----
    data = read_data("./2023/data/day21-input.txt")

    # Solution for part A
    print("\n-- Solution for part A:")
    print(part_one(data, 64))  # 3578

    # Solution for part B
    print("\n-- Solution for part B:")
    print(part_two(data, 26501365))  # 594115391548176
    # 26501365 = 2023 * 131 * 100 + 131//2 --> 100 grids + half grid * 2023
    # Given that the row and column of cell S only contain "." (no rock) and that the grid is a square
    # => it takes half_grid steps (131//2) to get to the next grid
    # => the diamond area increases following a quadratic function.
    # Solution = get 3 datapoints, then find coefficients of the quadratic function and apply it.
    # See explanations at: https://www.reddit.com/r/adventofcode/comments/18nevo3/comment/keaiiq7/
