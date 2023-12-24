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


def display_grid(grid: Grid) -> None:
    for line in grid:
        print("".join(line))


def find_start(grid: Grid) -> Position:
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == "S":
                return i, j

    raise ValueError("No start position in this grid! This should not happen.")


def find_neighbors(grid: Grid, position: Position) -> list[Position]:
    offsets = [(0, 1), (0, -1), (-1, 0), (1, 0)]
    neighbors = []
    for offset in offsets:
        x = position[0] + offset[0]
        y = position[1] + offset[1]
        if grid[x][y] == "#":
            continue
        neighbors.append((x, y))
    return neighbors


def update_grid(grid: Grid, to_remove: list[Position], to_add: set[Position]):
    # Remove
    for x, y in to_remove:
        grid[x][y] = "."
    # Add
    for x, y in to_add:
        grid[x][y] = "O"


def walk(grid: Grid, nb_steps: int) -> None:
    start = find_start(grid)

    queue = deque()
    queue.append([start])

    for step in range(nb_steps):
        # print("\n--- STEP", step)
        currents = queue.popleft()
        all_neighbors = set()
        for current in currents:
            neighbors = find_neighbors(grid, current)
            for neighbor in neighbors:
                all_neighbors.add(neighbor)

        update_grid(grid, currents, all_neighbors)
        # display_grid(grid)

        queue.append(all_neighbors)


def count_plots(grid: Grid) -> int:
    nb_plots = 0
    for row in grid:
        for cell in row:
            if cell == "O":
                nb_plots += 1
    return nb_plots


def part_one(data: str, nb_steps: int) -> int:
    grid = parse_data(data)
    # display_grid(grid)

    walk(grid, nb_steps)

    return count_plots(grid)


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

    # # Solution for part B
    # print("\n-- Solution for part B:")
    # print(part_two(data))  # 237878264003759
