def read_data(file_name):
    with open(file_name, 'r') as file:
        return [line.strip() for line in file.readlines()]


def parse_line(line: str):
    springs = line.split(" ")[0]
    counts = [int(i) for i in line.split(" ")[1].split(",")]
    return springs, counts


def get_counts(arrangement: str):
    counts = []
    current_count = 0
    for i in arrangement:
        if i == "#":
            current_count += 1
            continue
        if i == ".":
            counts.append(current_count)
            current_count = 0
            continue
    if arrangement[-1] == "#":
        counts.append(current_count)
    return [count for count in counts if count != 0]


def backtrack(springs: str, expected_counts: list[int], arrangement: str, arrangements: set[str] = ""):
    # print("arrangement", arrangement)
    if len(arrangement) == len(springs):
        actual_counts = get_counts(arrangement)
        # print(arrangement, actual_counts)
        if actual_counts != expected_counts:
            return
        arrangements.add(arrangement)
        return

    # Iterate all possible solutions
    # print("ITERATING")
    # for i in range(len(arrangement), len(springs)):
    i = len(arrangement)
    if springs[i] == "#" or springs[i] == ".":
        backtrack(springs, expected_counts, arrangement + springs[i], arrangements)
    else:
        # Try "#"
        backtrack(springs, expected_counts, arrangement + "#", arrangements)
        # Try "."
        backtrack(springs, expected_counts, arrangement + ".", arrangements)


def count_arrangements(springs: str, expected_counts: list[int]) -> int:
    arrangements = set()
    backtrack(springs, expected_counts, arrangement="", arrangements=arrangements)
    # print(arrangements)
    return len(arrangements)


def part_one(data: list[str]) -> int:
    total = 0
    for line in data:
        springs, counts = parse_line(line)
        total += count_arrangements(springs, counts)
    return total


if __name__ == "__main__":
    # ---- TEST DATA -----
    # SOME TESTS
    print(get_counts("###") == [3])
    print(get_counts("...") == [])
    print(get_counts(".#.") == [1])
    print(get_counts("##.") == [2])
    print(get_counts("#.#") == [1, 1])
    print(get_counts("#.#...") == [1, 1])
    print(get_counts("#.#.....###") == [1, 1, 3])

    test_data = [
        "???.### 1,1,3",
        ".??..??...?##. 1,1,3",
        "?#?#?#?#?#?#?#? 1,3,1,6",
        "????.#...#... 4,1,1",
        "????.######..#####. 1,6,5",
        "?###???????? 3,2,1"
    ]
    print("-- Tests on test data:")
    print(part_one(test_data) == 21)
    # print(part_two(test_data) == 525152)

    # ---- REAL DATA ----
    data = read_data("./2023/data/day12-input.txt")

    # Solution for part A
    print("\n-- Solution for part A:")
    print(part_one(data))  # 6488
    #
    # # Solution for part B
    # print("\n-- Solution for part B:")
    # print(part_two(data))  # 827009909817
