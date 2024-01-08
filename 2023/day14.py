def read_data(file_name):
    with open(file_name, 'r') as file:
        return [line.strip() for line in file.readlines()]


def get_rocks(grid: list[list[str]], shape: str) -> list[tuple[int, int]]:
    rocks = []
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == shape:
                rocks.append((i, j))

    return rocks


def get_new_position(position: tuple[int, int], direction: str) -> tuple[int, int]:
    if direction == "N":
        return position[0] - 1, position[1]
    if direction == "W":
        return position[0], position[1] - 1
    if direction == "S":
        return position[0] + 1, position[1]
    if direction == "E":
        return position[0], position[1] + 1
    raise ValueError("SHOULD NOT HAPPEN")


def can_move(position: tuple[int, int], direction: str, grid: list[list[str]]) -> bool:
    if direction == "N":
        return position[0] >= 0
    if direction == "W":
        return position[1] >= 0
    if direction == "S":
        return position[0] < len(grid)
    if direction == "E":
        return position[1] < len(grid[0])
    raise ValueError("SHOULD NOT HAPPEN")


def move_rock(position, filled_positions, direction: str, grid: list[list[str]]):
    new_position = get_new_position(position, direction)
    while can_move(new_position, direction, grid) and new_position not in filled_positions:
        filled_positions.remove(position)
        filled_positions.add(new_position)
        position = new_position
        new_position = get_new_position(new_position, direction)


def move_north(grid: list[list[str]]) -> set[tuple[int, int]]:
    cube_rocks = get_rocks(grid, "#")
    rounded_rocks = get_rocks(grid, "O")
    filled_positions = set(cube_rocks).union(set(rounded_rocks))

    for col in range(len(grid[0])):
        for row in range(len(grid)):
            cell = grid[row][col]
            if cell == "#" or cell == ".":
                continue
            move_rock(position=(row, col), filled_positions=filled_positions, direction="N", grid=grid)

    return filled_positions


def move_south(grid: list[list[str]]) -> set[tuple[int, int]]:
    cube_rocks = get_rocks(grid, "#")
    rounded_rocks = get_rocks(grid, "O")
    filled_positions = set(cube_rocks).union(set(rounded_rocks))

    for col in range(len(grid[0])):
        for row in reversed(range(len(grid))):
            cell = grid[row][col]
            if cell == "#" or cell == ".":
                continue
            move_rock(position=(row, col), filled_positions=filled_positions, direction="S", grid=grid)

    return filled_positions


def move_west(grid: list[list[str]]) -> set[tuple[int, int]]:
    cube_rocks = get_rocks(grid, "#")
    rounded_rocks = get_rocks(grid, "O")
    filled_positions = set(cube_rocks).union(set(rounded_rocks))

    for row in range(len(grid)):
        for col in range(len(grid[0])):
            cell = grid[row][col]
            if cell == "#" or cell == ".":
                continue
            move_rock(position=(row, col), filled_positions=filled_positions, direction="W", grid=grid)

    return filled_positions


def move_east(grid: list[list[str]]) -> set[tuple[int, int]]:
    cube_rocks = get_rocks(grid, "#")
    rounded_rocks = get_rocks(grid, "O")
    filled_positions = set(cube_rocks).union(set(rounded_rocks))

    for row in range(len(grid)):
        for col in reversed(range(len(grid[0]))):
            cell = grid[row][col]
            if cell == "#" or cell == ".":
                continue
            move_rock(position=(row, col), filled_positions=filled_positions, direction="E", grid=grid)

    return filled_positions


def create_grid(grid: list[list[str]], filled_positions: set[tuple[int, int]]) -> list[list[str]]:
    new_grid = []
    for i, row in enumerate(grid):
        new_row = []
        for j, cell in enumerate(row):
            if cell == "O" or cell == ".":
                if (i, j) in filled_positions:
                    new_row.append("O")
                else:
                    new_row.append(".")
            if cell == "#":
                new_row.append("#")
        new_grid.append(new_row)
        # print(new_row)
    return new_grid


def compute_score(grid: list[list[str]]) -> int:
    score = 0
    max_i = len(grid)
    for i, row in enumerate(grid):
        for cell in row:
            if cell == "O":
                score += max_i - i
    return score


def part_one(data: list[str]) -> int:
    table = [list(line) for line in data]
    filled_positions = move_north(table)
    new_grid = create_grid(table, filled_positions)
    return compute_score(new_grid)


def cycle_north(grid: list[list[str]]) -> list[list[str]]:
    filled_positions = move_north(grid)
    return create_grid(grid, filled_positions)


def cycle_south(grid: list[list[str]]) -> list[list[str]]:
    filled_positions = move_south(grid)
    return create_grid(grid, filled_positions)


def cycle_west(grid: list[list[str]]) -> list[list[str]]:
    filled_positions = move_west(grid)
    return create_grid(grid, filled_positions)


def cycle_east(grid: list[list[str]]) -> list[list[str]]:
    filled_positions = move_east(grid)
    return create_grid(grid, filled_positions)


def perform_cycle(grid: list[list[str]]) -> list[list[str]]:
    gridN = cycle_north(grid)
    gridW = cycle_west(gridN)
    gridS = cycle_south(gridW)
    gridE = cycle_east(gridS)

    return gridE


def display(grid: list[list[str]], i):
    print("\nAFTER CYCLE", i)
    for row in grid:
        print("".join(row))


def find_period(array: list[int], start=0) -> tuple[int, list[int]]:
    period_min_length = 1
    repetitions = 5  # Assuming OK if repeated 5 times
    for i in range(period_min_length, 2**10):
        sequence0 = array[start: start + i]
        for rep in range(1, repetitions):
            sequence = array[start + i * rep: start + (rep + 1) * i]
            if sequence0 != sequence:
                break
        else:
            return i, sequence0

    raise ValueError("NO PERIOD FOUND")


def part_two(data: list[str]) -> int:
    grid = [list(line) for line in data]
    scores = []
    for i in range(500):
        grid = perform_cycle(grid)
        # display(grid, i)
        score = compute_score(grid)
        # print(score)
        scores.append(score)
    # print(scores)
    # init_phase is chosen arbitrarily - it needs to be big enough to have the system already stabilized
    init_phase = 100
    period, sequence = find_period(scores, start=init_phase)

    finish = 1000000000
    remaining = (finish - init_phase) % period - 1
    print("Finish:", finish, "remaining", remaining, "Period", period, "result", sequence[remaining])
    return sequence[remaining]



if __name__ == "__main__":
    # ---- TEST DATA -----
    test_data = [
        "O....#....",
        "O.OO#....#",
        ".....##...",
        "OO.#O....O",
        ".O.....O#.",
        "O.#..O.#.#",
        "..O..#O..O",
        ".......O..",
        "#....###..",
        "#OO..#...."
    ]
    print("-- Tests on test data:")
    print(part_one(test_data) == 136)
    print(part_two(test_data) == 64)

    # ---- REAL DATA ----
    data = read_data("./data/2023/day14-input.txt")

    # Solution for part A
    print("\n-- Solution for part A:")
    print(part_one(data))  # 108792

    # Solution for part B
    print("\n-- Solution for part B:")
    print(part_two(data))  # 99118
