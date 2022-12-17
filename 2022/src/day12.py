import math


def read_data(file_name):
    with open(file_name, 'r') as file:
        return [line.strip() for line in file.readlines()]


def compute_ord_value(character):
    # Special cases for Start and End
    if character == "E":
        return ord('z')
    if character == "S":
        return ord('a')
    return ord(character)


# Compute all candidate neighbors on N, S, E, W directions
def compute_all_neighbors(grid, cell_position):
    [cell_row, cell_col] = cell_position
    neighbors = []
    N_neighbor = (cell_row - 1, cell_col)
    S_neighbor = (cell_row + 1, cell_col)
    E_neighbor = (cell_row, cell_col + 1)
    W_neighbor = (cell_row, cell_col - 1)

    if cell_row > 0:
        neighbors.append(N_neighbor)
    if cell_row < len(grid) - 1:
        neighbors.append(S_neighbor)
    if cell_col > 0:
        neighbors.append(W_neighbor)
    if cell_col < len(grid[0]) - 1:
        neighbors.append(E_neighbor)

    return neighbors


# Valid neighbors are those for which we have to jump only one step up OR jump down (by any amount of steps)
def select_valid_neighbors(candidate_neighbors, grid, cell_position):
    cell_value = compute_ord_value(grid[cell_position[0]][cell_position[1]])
    neighbors = []
    for candidate_neighbor in candidate_neighbors:
        [row, col] = candidate_neighbor
        candidate_neighbor_value = compute_ord_value(grid[row][col])

        jump_one_step_up = candidate_neighbor_value == cell_value - 1
        jump_down = candidate_neighbor_value >= cell_value

        if jump_one_step_up or jump_down:
            neighbors.append(candidate_neighbor)

    return neighbors


# steps = the number of moves away from the endpoint
def compute_steps(grid, end_position):  # bfs
    frontier_cells_to_visit = [end_position]
    steps = {}
    steps[end_position] = 0

    # For each cell in the frontier, I want:
    # 1. find all neighbors
    # 2. for each neighbor,
    #    if already visited (= steps defined for this cell) => do nothing
    #    else => IF it is a valid neighbor (= one onto which we can jump) => step = step + 1, else, do nothing
    while len(frontier_cells_to_visit) > 0:
        # Deal with first cell of the list
        cell_position = frontier_cells_to_visit.pop(0)

        # Find all valid neighbors (= those onto which we can jump from the current cell)
        candidate_neighbors = compute_all_neighbors(grid, cell_position)
        neighbors = select_valid_neighbors(candidate_neighbors, grid, cell_position)

        for neighbor in neighbors:
            # If not already visited, append it to the list and compute it step number
            if neighbor not in steps:
                frontier_cells_to_visit.append(neighbor)
                steps[neighbor] = steps[cell_position] + 1

    return steps


def find_position(grid, character):
    for row_index, row in enumerate(grid):
        for col_index, col in enumerate(list(row)):
            if col == character:
                return (row_index, col_index)


def part_one(grid):
    start_position = find_position(grid, 'S')
    end_position = find_position(grid, 'E')
    print("Start position is", start_position)
    print("End position is", end_position)

    steps = compute_steps(grid, end_position)
    # print("cell_levels", cell_levels)

    return steps[start_position]


def find_all_positions(grid, character):
    all_positions = []
    for row_index, row in enumerate(grid):
        for col_index, col in enumerate(list(row)):
            if col == character:
                all_positions.append((row_index, col_index))

    return all_positions


def part_two(grid):
    all_possible_starting_points = find_all_positions(grid, 'a') + [find_position(grid, 'S')]
    end_position = find_position(grid, 'E')

    steps = compute_steps(grid, end_position)

    min_steps = math.inf
    for possible_starting_point in all_possible_starting_points:
        if possible_starting_point in steps:
            min_steps = min(min_steps, steps[possible_starting_point])

    return min_steps


if __name__ == "__main__":
    # ---- TEST DATA -----
    test_data = [
        "Sabqponm",
        "abcryxxl",
        "accszExk",
        "acctuvwj",
        "abdefghi"
    ]
    print("-- Tests on test data:")
    print(part_one(test_data) == 31)
    print(part_two(test_data) == 29)

    # ---- REAL DATA ----
    data = read_data("./2022/data/day12-input.txt")

    # Solution for part A
    print("\n-- Solution for part A:")
    print(part_one(data))  # 447

    # Solution for part B
    print("\n-- Solution for part B:")
    print(part_two(data))  # 446
