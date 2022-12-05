def read_data(file_name):
    with open(file_name, 'r') as file:
        lines = [line.strip().split(",") for line in file.readlines()]
        split_lines = [[range1.split("-"), range2.split("-")] for [range1, range2] in lines]
        return [((int(range1[0]), int(range1[1])), (int(range2[0]), int(range2[1]))) for [range1, range2] in
                split_lines]


def part_one(data):
    nb_inclusions = 0
    for ((start_range1, end_range1), (start_range2, end_range2)) in data:
        if (start_range1 <= start_range2 and end_range1 >= end_range2) or (
                start_range1 >= start_range2 and end_range1 <= end_range2):
            nb_inclusions += 1

    return nb_inclusions


def part_two(data):
    nb_overlaps = 0
    for ((start_range1, end_range1), (start_range2, end_range2)) in data:
        if (start_range1 <= start_range2 <= end_range1) or (
                start_range2 <= start_range1 <= end_range2):
            nb_overlaps += 1

    return nb_overlaps


if __name__ == "__main__":
    # ---- TEST DATA -----
    test_data = [
        ((2, 4), (6, 8)),
        ((2, 3), (4, 5)),
        ((5, 7), (7, 9)),
        ((2, 8), (3, 7)),
        ((6, 6), (4, 6)),
        ((2, 6), (4, 8)),
    ]
    print("-- Tests on test data:")
    print(part_one(test_data) == 2)
    print(part_two(test_data) == 4)

    # ---- REAL DATA ----
    data = read_data("./2022/data/day04-input.txt")

    # Solution for 2-a
    print("\n-- Solution for 2-a:")
    print(part_one(data))

    # Solution for 2-b
    print("\n-- Solution for 2-b:")
    print(part_two(data))

# TODO: add complexity
