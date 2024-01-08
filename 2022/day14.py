def read_data(file_name):
    with open(file_name, 'r') as file:
        lines = [line.strip().split(" -> ") for line in file.readlines()]
        data = []
        for line in lines:
            positions = []
            for position in line:
                distance, depth = position.split(",")
                positions.append((int(distance), int(depth)))
            data.append(positions)
        return data


def draw_grid(grid):
    for row in grid:
        print("".join(row))


def find_grid_dimensions(rock_paths):
    grid_depth = 0
    grid_left = 500
    grid_right = 500
    for rock_path in rock_paths:
        for (x, y) in rock_path:
            grid_depth = max(grid_depth, y)
            grid_right = max(grid_right, x)
            grid_left = min(grid_left, x)

    return (grid_left, grid_right, grid_depth)


def update_grid_dimensions_with_floor(grid_left, grid_right, grid_depth):
    grid_depth = grid_depth + 2
    grid_width = 2 * (grid_depth + 1)
    grid_left = min(grid_left, 500 - grid_width // 2)
    grid_right = max(grid_right, 500 + grid_width // 2)

    return (grid_left, grid_right, grid_depth)


def add_path(grid, edge_1, edge_2, grid_left):
    dist_1, depth_1 = edge_1
    dist_2, depth_2 = edge_2
    # Horizontal case
    if depth_1 == depth_2:
        for i in range(min(dist_1, dist_2), max(dist_1, dist_2) + 1):
            grid[depth_1][i - grid_left] = "#"
    # Vertical case
    if dist_1 == dist_2:
        for i in range(min(depth_1, depth_2), max(depth_1, depth_2) + 1):
            grid[i][dist_1 - grid_left] = "#"


def define_cave_grid(rock_paths, grid_left, grid_right, grid_depth):
    # Initialise grid
    grid = []
    for y in range(0, grid_depth + 1):
        grid.append(["."] * (grid_right - grid_left + 1))
    grid[0][500 - grid_left] = "+"

    # Add rock lines
    for rock_path_edges in rock_paths:
        for i in range(len(rock_path_edges) - 1):
            edge_1 = rock_path_edges[i]
            edge_2 = rock_path_edges[i + 1]
            add_path(grid, edge_1, edge_2, grid_left)

    return grid


def find_rest_position(grid, sand_position, grid_left):
    dist, depth = sand_position
    below = (dist, depth + 1)
    below_left = (dist - 1, depth + 1)
    below_right = (dist + 1, depth + 1)

    # Stop if ouf of grid
    grid_depth = len(grid)
    grid_right = grid_left + len(grid[0])
    if (dist - 1 < grid_left) or (grid_right < dist + 1) or (depth + 1 >= grid_depth):
        return None

    # print(sand_position, "current", grid[depth][dist - grid_left])
    if grid[below[1]][below[0] - grid_left] == ".":
        return find_rest_position(grid, below, grid_left)
    # else:
    if grid[below_left[1]][below_left[0] - grid_left] == ".":
        # Try left
        return find_rest_position(grid, below_left, grid_left)
    elif grid[below_right[1]][below_right[0] - grid_left] == ".":
        # Try right
        return find_rest_position(grid, below_right, grid_left)
    # else:
    # print("\nCurrent sand pos", sand_position, grid[depth][dist - grid_left])
    return sand_position


def add_sand_unit_in_grid(grid, sand_position, grid_left):
    if sand_position is None:
        return

    dist, depth = sand_position
    grid[depth][dist - grid_left] = "o"


def drop_sand_unit(grid, grid_left):
    initial_position = (500, 0)
    rest_position = find_rest_position(grid, initial_position, grid_left)
    add_sand_unit_in_grid(grid, rest_position, grid_left)
    # print("REST POS", rest_position)
    # draw_grid(grid)
    return rest_position


def count_number_sand_units_resting(grid, grid_left, finish_position):
    sand_units_resting = 0

    while True:
        new_rest_position = drop_sand_unit(grid, grid_left)
        if new_rest_position is finish_position:
            break
        sand_units_resting += 1

    return sand_units_resting


def part_one(rock_paths):
    # 1. define cave grid
    # 2. for each sand, move it to position (while)
    # 3. if no resting position => stop
    (grid_left, grid_right, grid_depth) = find_grid_dimensions(rock_paths)
    grid = define_cave_grid(rock_paths, grid_left, grid_right, grid_depth)
    # print("\nInitial grid:")
    # draw_grid(grid)
    # print("END GRID\n")

    number_sand_units_resting = count_number_sand_units_resting(grid, grid_left, None)
    # draw_grid(grid)

    return number_sand_units_resting


def part_two(rock_paths):
    (grid_left, grid_right, grid_depth) = find_grid_dimensions(rock_paths)
    (grid_left, grid_right, grid_depth) = update_grid_dimensions_with_floor(grid_left, grid_right, grid_depth)
    rock_paths.append([(grid_left, grid_depth), (grid_right, grid_depth)])
    grid = define_cave_grid(rock_paths, grid_left, grid_right, grid_depth)
    # print("\nInitial grid:")
    # draw_grid(grid)
    # print("END GRID\n")

    number_sand_units_resting = count_number_sand_units_resting(grid, grid_left, (500, 0)) + 1
    # draw_grid(grid)

    return number_sand_units_resting


if __name__ == "__main__":
    # ---- TEST DATA -----
    test_data = [
        [(498, 4), (498, 6), (496, 6)],
        [(503, 4), (502, 4), (502, 9), (494, 9)]
    ]
    print("-- Tests on test data:")
    print(part_one(test_data) == 24)
    print(part_two(test_data) == 93)

    # ---- REAL DATA ----
    data = read_data("./2022/data/day14-input.txt")

    # Solution for part A
    print("\n-- Solution for part A:")
    print(part_one(data))  # 1330

    # Solution for part B
    print("\n-- Solution for part B:")
    print(part_two(data))  # 26139
