from typing import Optional


def read_data(file_name):
    with open(file_name, 'r') as file:
        return file.read()[:-1]


def count_differences(a1: str, a2: str) -> int:
    if len(a1) != len(a2):
        raise ValueError("Counting differences between arrays of different lengths: SHOULD NOT HAPPEN !")
    differences = 0
    for i in range(len(a1)):
        el1 = a1[i]
        el2 = a2[i]
        if el1 != el2:
            differences += 1
    return differences


def is_h_mirror(part: list[str], h_mirror: int, is_smudge_available: bool = False) -> bool:
    depth = min(h_mirror, len(part) - h_mirror)
    for d in range(0, depth):
        top = part[h_mirror - 1 - d]
        bottom = part[h_mirror + d]
        nb_differences = count_differences(top, bottom)
        if nb_differences > 1:
            return False
        if nb_differences == 1:
            if is_smudge_available:
                is_smudge_available = False
                continue
            return False
    return True


def find_horizontal_mirror(part: list[str], is_smudge_available: bool = False, original: int = None) -> Optional[int]:
    for h_mirror in range(1, len(part)):
        if h_mirror == original:
            continue
        if is_h_mirror(part, h_mirror, is_smudge_available):
            return h_mirror
    return None


def is_v_mirror(part: list[str], v_mirror: int, is_smudge_available: bool = False) -> bool:
    depth = min(v_mirror, len(part[0]) - v_mirror)
    for d in range(0, depth):
        left = "".join([line[v_mirror - 1 - d] for line in part])
        right = "".join([line[v_mirror + d] for line in part])
        nb_differences = count_differences(left, right)
        if nb_differences > 1:
            return False
        if nb_differences == 1:
            if is_smudge_available:
                is_smudge_available = False
                continue
            return False
    return True


def find_vertical_mirror(part: list[str], is_smudge_available: bool = False, original: int = None) -> Optional[int]:
    for v_mirror in range(1, len(part[0])):
        if v_mirror == original:
            continue
        if is_v_mirror(part, v_mirror, is_smudge_available):
            return v_mirror
    return None


def part_one(data: str) -> int:
    parts = data.split("\n\n")
    total = 0
    for part in parts:
        part_lines = part.split("\n")
        nb_rows_before_mirror = find_horizontal_mirror(part_lines)
        if nb_rows_before_mirror is not None:
            total += 100 * nb_rows_before_mirror
        else:
            nb_cols_before_mirror = find_vertical_mirror(part_lines)
            if nb_cols_before_mirror is None:
                raise ValueError("No horizontal nor vertical reflection line: SHOULD NOT HAPPEN !")
            total += nb_cols_before_mirror
    return total


def part_two(data: str) -> int:
    parts = data.split("\n\n")
    total = 0
    for part in parts:
        part_lines = part.split("\n")
        original_nb_rows = find_horizontal_mirror(part_lines, is_smudge_available=False)
        nb_rows_before_mirror = find_horizontal_mirror(part_lines, is_smudge_available=True, original=original_nb_rows)
        if nb_rows_before_mirror is not None:
            if original_nb_rows == nb_rows_before_mirror:
                raise ValueError("Horizontal reflection line is the same with and without smudge: SHOULD NOT HAPPEN !")
            total += 100 * nb_rows_before_mirror
        else:
            original_nb_cols = find_vertical_mirror(part_lines, is_smudge_available=False)
            nb_cols_before_mirror = find_vertical_mirror(part_lines, is_smudge_available=True,
                                                         original=original_nb_cols)
            if nb_cols_before_mirror is None:
                raise ValueError("No horizontal nor vertical reflection line: SHOULD NOT HAPPEN !")
            if original_nb_cols == nb_cols_before_mirror:
                raise ValueError("Vertical reflection line is the same with and without smudge: SHOULD NOT HAPPEN !")
            total += nb_cols_before_mirror
    return total


if __name__ == "__main__":
    # ---- TEST DATA -----
    test_data = '''#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#'''
    print("-- Tests on test data:")
    print(part_one(test_data) == 405)
    print(part_two(test_data) == 400)

    # ---- REAL DATA ----
    data = read_data("./data/2023/day13-input.txt")

    # Solution for part A
    print("\n-- Solution for part A:")
    print(part_one(data))  # 31877

    # Solution for part B
    print("\n-- Solution for part B:")
    print(part_two(data))  # 42996
