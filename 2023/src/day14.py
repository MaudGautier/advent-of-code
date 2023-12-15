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


def move_rock_north(position, filled_positions):
    north_position = (position[0] - 1, position[1])
    while north_position[0] >= 0 and north_position not in filled_positions:
        filled_positions.remove(position)
        filled_positions.add(north_position)
        position = north_position
        north_position = (north_position[0] - 1, north_position[1])


def move_north(grid: list[list[str]]) -> set[tuple[int, int]]:
    cube_rocks = get_rocks(grid, "#")
    rounded_rocks = get_rocks(grid, "O")
    filled_positions = set(cube_rocks).union(set(rounded_rocks))

    for col in range(len(grid[0])):
        for row in range(len(grid)):
            cell = grid[row][col]
            if cell == "#" or cell == ".":
                continue
            move_rock_north(position=(row, col), filled_positions=filled_positions)

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
    # print(part_two(test_data) == 374)

    # ---- REAL DATA ----
    data = read_data("./2023/data/day14-input.txt")

    # Solution for part A
    print("\n-- Solution for part A:")
    print(part_one(data))  # 108792
    #
    # # Solution for part B
    # print("\n-- Solution for part B:")
    # print(part_two(data))  # 827009909817
