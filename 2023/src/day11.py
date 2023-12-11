from collections import deque


def read_data(file_name):
    with open(file_name, 'r') as file:
        return [line.strip() for line in file.readlines()]


def find_rows_and_cols_without_galaxies(universe: list[str]) -> tuple[list[int], list[int]]:
    cols_with_galaxies = set()
    rows_with_galaxies = set()
    for row_index, row in enumerate(universe):
        for col_index, col in enumerate(row):
            if universe[row_index][col_index] == "#":
                cols_with_galaxies.add(col_index)
                rows_with_galaxies.add(row_index)
    rows_without_galaxies = set(range(len(universe))) - rows_with_galaxies
    cols_without_galaxies = set(range(len(universe[0]))) - cols_with_galaxies
    return sorted(list(rows_without_galaxies)), sorted(list(cols_without_galaxies))


def expand_universe(universe: list[str]) -> list[str]:
    rows_without_galaxies, cols_without_galaxies = find_rows_and_cols_without_galaxies(universe)

    expanded_universe = []
    for row_index, row in enumerate(universe):
        expanded_row = "".join(
            [cell if cell_index not in cols_without_galaxies else '..' for cell_index, cell in enumerate(row)])
        expanded_universe.append(expanded_row)
        if row_index in rows_without_galaxies:
            expanded_universe.append(expanded_row)

    return expanded_universe


def find_galaxies(universe: list[str]) -> list[tuple[int, int]]:
    galaxies = []
    for row_index, row in enumerate(universe):
        for col_index, cell in enumerate(row):
            if cell == "#":
                galaxies.append((row_index, col_index))
    return galaxies


def find_neighbors(universe: list[str], position: tuple[int, int]) -> list[tuple[int, int]]:
    offsets = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    neighbors = []
    for offset in offsets:
        row = position[0] + offset[0]
        col = position[1] + offset[1]
        if 0 <= row < len(universe) and 0 <= col < len(universe[0]):
            neighbors.append((row, col))
    return neighbors


def compute_depth(neighbor, depth, rows_without_galaxies, cols_without_galaxies, expansion):
    if neighbor[0] in rows_without_galaxies:
        return depth + expansion
    if neighbor[1] in cols_without_galaxies:
        return depth + expansion

    return depth + 1


def bfs2(universe: list[str], start: tuple[int, int], galaxies: list[tuple[int, int]], rows_without_galaxies: set[int],
         cols_without_galaxies: set[int], expansion: int) -> int:
    visited = set()
    to_visit = deque()  # queue
    to_visit.append((start, 0))
    total = 0
    count = 0
    while len(to_visit) > 0 and count < len(galaxies):
        position, depth = to_visit.popleft()
        if position in visited:
            continue
        visited.add(position)
        if position in galaxies:
            count += 1
            total += depth
        for neighbor in find_neighbors(universe, position):
            new_depth = compute_depth(neighbor, depth, rows_without_galaxies, cols_without_galaxies, expansion)
            to_visit.append((neighbor, new_depth))

    return total


def part_one_and_two(universe: list[str], expansion: int = 2) -> int:
    rows_without_galaxies, cols_without_galaxies = find_rows_and_cols_without_galaxies(universe)

    galaxies = find_galaxies(universe)
    total = 0
    # print("TOTAL GALAXIES", len(galaxies))
    count = 0
    updates = 0
    for galaxy in galaxies:
        # Progress bar
        count += 1
        # print("Galaxy nº", count)
        finished = count * 100 // len(galaxies)
        if divmod(finished, 10) == (updates, 0):
            updates += 1
            print('Finished processing {} % of all galaxies'.format(int(finished)))

        # Logic
        paths_lengths = bfs2(universe, galaxy, galaxies, set(rows_without_galaxies), set(cols_without_galaxies),
                             expansion)
        total += paths_lengths

    return total // 2


if __name__ == "__main__":
    # ---- TEST DATA -----
    test_data = [
        "...#......",
        ".......#..",
        "#.........",
        "..........",
        "......#...",
        ".#........",
        ".........#",
        "..........",
        ".......#..",
        "#...#....."
    ]
    print("-- Tests on test data:")
    print(part_one_and_two(test_data) == 374)
    print(part_one_and_two(test_data, 2) == 374)
    print(part_one_and_two(test_data, 10) == 1030)
    print(part_one_and_two(test_data, 100) == 8410)

    # ---- REAL DATA ----
    data = read_data("./2023/data/day11-input.txt")

    # Solution for part A
    print("\n-- Solution for part A:")
    print(part_one_and_two(data))  # 9563821 # NOT OPTIMAL IN TIME ~ 1-2 mins to run

    # Solution for part B
    print("\n-- Solution for part B:")
    print(part_one_and_two(data, 1000000))  # 827009909817 # STILL NOT OPTIMAL IN TIME ~ 1-2 mins to run
