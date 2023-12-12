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


def find_galaxies(universe: list[str]) -> list[tuple[int, int]]:
    galaxies = []
    for row_index, row in enumerate(universe):
        for col_index, cell in enumerate(row):
            if cell == "#":
                galaxies.append((row_index, col_index))
    return galaxies


def compute_path_length(start: tuple[int, int], galaxies: list[tuple[int, int]], rows_without_galaxies: set[int],
                        cols_without_galaxies: set[int], expansion: int) -> int:
    paths_lengths = 0
    for galaxy in galaxies:
        path_length = abs(galaxy[0] - start[0]) + abs(galaxy[1] - start[1])
        min_row, max_row = min(galaxy[0], start[0]), max(galaxy[0], start[0])
        min_col, max_col = min(galaxy[1], start[1]), max(galaxy[1], start[1])

        nb_rows_to_expand = len(rows_without_galaxies.intersection(set(list(range(min_row + 1, max_row)))))
        nb_cols_to_expand = len(cols_without_galaxies.intersection(set(list(range(min_col + 1, max_col)))))
        path_length += nb_rows_to_expand * (expansion - 1) + nb_cols_to_expand * (expansion - 1)
        paths_lengths += path_length
    return paths_lengths


def part_one_and_two(universe: list[str], expansion: int = 2) -> int:
    rows_without_galaxies, cols_without_galaxies = find_rows_and_cols_without_galaxies(universe)

    galaxies = find_galaxies(universe)
    total = 0
    for galaxy in galaxies:
        paths_lengths = compute_path_length(galaxy, galaxies, set(rows_without_galaxies), set(cols_without_galaxies),
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
    print(part_one_and_two(data))  # 9563821

    # Solution for part B
    print("\n-- Solution for part B:")
    print(part_one_and_two(data, 1000000))  # 827009909817
