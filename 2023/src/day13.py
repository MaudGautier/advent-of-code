def read_data(file_name):
    with open(file_name, 'r') as file:
        return file.read()[:-1]


def is_h_mirror(part: list[str], h_mirror: int) -> bool:
    depth = min(h_mirror, len(part) - h_mirror)
    for d in range(0, depth):
        top = part[h_mirror - 1 - d]
        bottom = part[h_mirror + d]
        if top != bottom:
            return False
    return True


def find_horizontal_mirror(part: list[str]) -> int:
    for h_mirror in range(1, len(part)):
        if is_h_mirror(part, h_mirror):
            return h_mirror
    return 0


def is_v_mirror(part: list[str], v_mirror: int) -> bool:
    depth = min(v_mirror, len(part[0]) - v_mirror)
    for d in range(0, depth):
        for line in part:
            left = line[v_mirror - 1 - d]
            right = line[v_mirror + d]
            if left != right:
                return False
    return True


def find_vertical_mirror(part: list[str]) -> int:
    for v_mirror in range(1, len(part[0])):
        if is_v_mirror(part, v_mirror):
            return v_mirror
    return 0


def part_one(data: str) -> int:
    parts = data.split("\n\n")
    total = 0
    for part in parts:
        part_lines = part.split("\n")
        nb_cols_before_mirror = find_vertical_mirror(part_lines)
        nb_rows_before_mirror = find_horizontal_mirror(part_lines)
        total += nb_cols_before_mirror
        total += 100 * nb_rows_before_mirror
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
    # print(part_two(test_data, 2) == 374)

    # ---- REAL DATA ----
    data = read_data("./2023/data/day13-input.txt")

    # Solution for part A
    print("\n-- Solution for part A:")
    print(part_one(data))  # 31877
    #
    # # Solution for part B
    # print("\n-- Solution for part B:")
    # print(part_two(data, 1000000))  # 827009909817
