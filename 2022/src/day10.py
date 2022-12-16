def read_data(file_name):
    with open(file_name, 'r') as file:
        return [line.strip() for line in file.readlines()]


def compute_cycle_register(instructions):
    # cycle = 0
    register_value = 1
    during_cyle_register = [1]
    for instruction in instructions:
        # cycle += 1
        # if cycle in [20, 60, 100, 140, 180, 220]:
        #     print("@@DURING of cycle", cycle, register_value, cycle * register_value)
        during_cyle_register.append(register_value)
        if instruction == "noop":
            continue
        else:
            # cycle += 1
            # if cycle in [20, 60, 100, 140, 180, 220]:
            #     print("**DURING of cycle", cycle, register_value, cycle * register_value)
            during_cyle_register.append(register_value)
            increment = int(instruction.split(" ")[1])
            register_value += increment

    return during_cyle_register


def part_one(instructions):
    cycle_register = compute_cycle_register(instructions)
    total = 0
    for i in [20, 60, 100, 140, 180, 220]:
        total += i * cycle_register[i]
    return total


if __name__ == "__main__":
    # ---- TEST DATA -----
    test_data = [
        "addx 15",
        "addx -11",
        "addx 6",
        "addx -3",
        "addx 5",
        "addx -1",
        "addx -8",
        "addx 13",
        "addx 4",
        "noop",
        "addx -1",
        "addx 5",
        "addx -1",
        "addx 5",
        "addx -1",
        "addx 5",
        "addx -1",
        "addx 5",
        "addx -1",
        "addx -35",
        "addx 1",
        "addx 24",
        "addx -19",
        "addx 1",
        "addx 16",
        "addx -11",
        "noop",
        "noop",
        "addx 21",
        "addx -15",
        "noop",
        "noop",
        "addx -3",
        "addx 9",
        "addx 1",
        "addx -3",
        "addx 8",
        "addx 1",
        "addx 5",
        "noop",
        "noop",
        "noop",
        "noop",
        "noop",
        "addx -36",
        "noop",
        "addx 1",
        "addx 7",
        "noop",
        "noop",
        "noop",
        "addx 2",
        "addx 6",
        "noop",
        "noop",
        "noop",
        "noop",
        "noop",
        "addx 1",
        "noop",
        "noop",
        "addx 7",
        "addx 1",
        "noop",
        "addx -13",
        "addx 13",
        "addx 7",
        "noop",
        "addx 1",
        "addx -33",
        "noop",
        "noop",
        "noop",
        "addx 2",
        "noop",
        "noop",
        "noop",
        "addx 8",
        "noop",
        "addx -1",
        "addx 2",
        "addx 1",
        "noop",
        "addx 17",
        "addx -9",
        "addx 1",
        "addx 1",
        "addx -3",
        "addx 11",
        "noop",
        "noop",
        "addx 1",
        "noop",
        "addx 1",
        "noop",
        "noop",
        "addx -13",
        "addx -19",
        "addx 1",
        "addx 3",
        "addx 26",
        "addx -30",
        "addx 12",
        "addx -1",
        "addx 3",
        "addx 1",
        "noop",
        "noop",
        "noop",
        "addx -9",
        "addx 18",
        "addx 1",
        "addx 2",
        "noop",
        "noop",
        "addx 9",
        "noop",
        "noop",
        "noop",
        "addx -1",
        "addx 2",
        "addx -37",
        "addx 1",
        "addx 3",
        "noop",
        "addx 15",
        "addx -21",
        "addx 22",
        "addx -6",
        "addx 1",
        "noop",
        "addx 2",
        "addx 1",
        "noop",
        "addx -10",
        "noop",
        "noop",
        "addx 20",
        "addx 1",
        "addx 2",
        "addx 2",
        "addx -6",
        "addx -11",
        "noop",
        "noop",
        "noop",

    ]
    print("-- Tests on test data:")
    print(part_one(test_data) == 13140)
    # print(part_two(test_data) == 1)

    # ---- REAL DATA ----
    data = read_data("./2022/data/day10-input.txt")

    # Solution for part A
    print("\n-- Solution for part A:")
    print(part_one(data))  # 12880
    #
    # # Solution for part B
    # print("\n-- Solution for part B:")
    # print(part_two(data))  # 2434
