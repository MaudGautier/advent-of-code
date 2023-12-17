def read_data(file_name):
    with open(file_name, 'r') as file:
        return [line.strip() for line in file.readlines()]


def parse_line(line: str):
    springs = line.split(" ")[0]
    counts = [int(i) for i in line.split(" ")[1].split(",")]
    return springs, tuple(counts)


def parse_line_part_two(line: str, expansion: int = 0):
    springs = line.split(" ")[0]
    counts = [int(i) for i in line.split(" ")[1].split(",")]
    unfolded_springs = (springs + "?") * expansion + springs
    unfolded_counts = counts * (expansion + 1)
    return unfolded_springs, tuple(unfolded_counts)


def part_one(data: list[str]) -> int:
    total = 0
    for line in data:
        springs, counts = parse_line(line)
        total += count_nb_valid_arrangements(springs, counts)
    return total


MEMO = {}


# Dynamic programming - recursion
def count_nb_valid_arrangements(springs: str, expected_counts: tuple[int]) -> int:
    if (springs, expected_counts) in MEMO:
        return MEMO[(springs, expected_counts)]

    # Base case - if no more groups => springs must contain no "#"
    if len(expected_counts) == 0:
        return "#" not in springs
    # Base case - if no more springs => there must be no expected counts
    if len(springs) == 0:
        return len(expected_counts) == 0

    # Recursion
    spring, rest_springs = springs[0], springs[1:]

    if spring == ".":
        result = count_nb_valid_arrangements(rest_springs, expected_counts)
        MEMO[(springs, expected_counts)] = result
        return result

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
            result = count_nb_valid_arrangements(springs[expected_count + 1:], expected_counts[1:])
            MEMO[(springs, expected_counts)] = result
            return result
        MEMO[(springs, expected_counts)] = 0
        return 0

    if spring == "?":
        result = (
                count_nb_valid_arrangements(f".{rest_springs}", expected_counts)  # Case 1: replaced by "."
                + count_nb_valid_arrangements(f"#{rest_springs}", expected_counts)  # Case 2: replaced by "#"
        )
        MEMO[(springs, expected_counts)] = result
        return result

    raise ValueError("SHOULD NOT GET HERE")


def part_two(data: list[str]) -> int:
    total = 0
    for i, line in enumerate(data):
        springs, counts = parse_line_part_two(line, 4)
        counted = count_nb_valid_arrangements(springs, counts)
        total += counted

    return total


if __name__ == "__main__":
    # ---- TEST DATA -----
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
