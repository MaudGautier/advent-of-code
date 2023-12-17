from functools import cache


def read_data(file_name):
    with open(file_name, 'r') as file:
        return [line.strip() for line in file.readlines()]


def parse_line(line: str):
    springs = line.split(" ")[0]
    counts = [int(i) for i in line.split(" ")[1].split(",")]
    return springs, counts


def parse_line_part_two(line: str, expansion: int = 0):
    springs = line.split(" ")[0]
    counts = [int(i) for i in line.split(" ")[1].split(",")]
    unfolded_springs = (springs + "?") * expansion + springs
    unfolded_counts = counts * (expansion + 1)
    return unfolded_springs, tuple(unfolded_counts)


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
    if len(arrangement) and arrangement[-1] == "#":
        counts.append(current_count)
    return [count for count in counts if count != 0]


def backtrack(springs: str, expected_counts: list[int], arrangement: str, arrangements: set[str] = ""):
    actual_counts = get_counts(arrangement)[:-1]
    if actual_counts != expected_counts[:len(actual_counts)]:
        return

    if len(arrangement) == len(springs):
        actual_counts = get_counts(arrangement)
        if actual_counts != expected_counts:
            return
        arrangements.add(arrangement)
        return

    # Iterate all possible solutions
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
    return len(arrangements)


def part_one(data: list[str]) -> int:
    total = 0
    for line in data:
        springs, counts = parse_line(line)
        total += count_arrangements(springs, counts)
    return total


# Dynamic programming - recursion
@cache
def count_nb_valid_arrangements(springs: str, expected_counts: tuple[int]) -> int:
    # Base case - if no more groups => springs must contain no "#"
    if len(expected_counts) == 0:
        return "#" not in springs
    # Base case - if no more springs => there must be no expected counts
    if len(springs) == 0:
        return len(expected_counts) == 0

    # Recursion
    spring, rest_springs = springs[0], springs[1:]

    if spring == ".":
        return count_nb_valid_arrangements(rest_springs, expected_counts)

    if spring == "#":
        expected_count = expected_counts[0]
        if (
                # At least expected_count springs left (to create the group of springs)
                len(springs) >= expected_count
                # Only "#" or "?" in the next expected_counts springs (to create the group of springs)
                and (all(char in ["#", "?"] for char in springs[:expected_count]))
                # Either "." or "?" in the next expected_counts + 1 spring (to terminate the group of springs)
                # Or spring is finished
                and (len(springs) == expected_count or springs[expected_count] in [".", "?"])
        ):
            return count_nb_valid_arrangements(springs[expected_count + 1:], expected_counts[1:])
        return 0

    if spring == "?":
        return (
                count_nb_valid_arrangements(f".{rest_springs}", expected_counts)  # Case 1: replaced by "."
                + count_nb_valid_arrangements(f"#{rest_springs}", expected_counts)  # Case 2: replaced by "#"
        )

    raise ValueError("SHOULD NOT GET HERE")


def part_two(data: list[str]) -> int:
    total = 0
    for i, line in enumerate(data):
        print(i, "/", len(data))
        springs, counts = parse_line_part_two(line, 4)
        counted = count_nb_valid_arrangements(springs, counts)
        total += counted

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
    print(part_two(test_data) == 525152)

    # ---- REAL DATA ----
    data = read_data("./2023/data/day12-input.txt")

    # Solution for part A
    print("\n-- Solution for part A:")
    print(part_one(data))  # 6488

    # Solution for part B
    print("\n-- Solution for part B:")
    print(part_two(data))  # 815364548481

    # OBSERVATION on first attempt for optimisation of part B:
    # At any increase of expansion => multiply by a given number
    # => We need to have the computation for expansion 0 and expansion 1 -> compute the division, then do this 5 times
