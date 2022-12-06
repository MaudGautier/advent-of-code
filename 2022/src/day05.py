def get_stacks_and_instructions(lines):
    stacks = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: []}
    instructions = []
    for line in lines:
        if line.startswith("move"):
            infos = line.strip().split(" ")
            nb = int(infos[1])
            origin_stack = int(infos[3])
            destination_stack = int(infos[5])
            for i in range(nb):
                instructions.append((origin_stack, destination_stack))
        elif not line.startswith(" 1"):
            starts = [x * 4 for x in range((len(line) + 1) // 4)]
            for start in starts:
                item = line[1 + start]
                stack_index = int(start / 4) + 1
                if item != ' ':
                    stacks[stack_index].insert(0, item)

    return (stacks, instructions)


def read_data(file_name):
    with open(file_name, 'r') as file:
        lines = [line for line in file.readlines()]
        return lines


def part_one(stacks, instructions):
    # print(stacks)
    for instruction in instructions:
        origin_stack = instruction[0]
        destination_stack = instruction[1]
        item = stacks[origin_stack].pop()
        stacks[destination_stack].append(item)
        # print(instruction, "--->", stacks)

    top_items = ''
    for stack_index in range(1, 10):
        if len(stacks[stack_index]) >= 1:
            top_items += stacks[stack_index][-1]

    return top_items


def get_stacks_and_instructions_part_two(lines):
    stacks = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: []}
    instructions = []
    for line in lines:
        # Modify only instructions
        if line.startswith("move"):
            infos = line.strip().split(" ")
            nb = int(infos[1])
            origin_stack = int(infos[3])
            destination_stack = int(infos[5])
            instructions.append((origin_stack, destination_stack, nb))
        elif not line.startswith(" 1"):
            starts = [x * 4 for x in range((len(line) + 1) // 4)]
            for start in starts:
                item = line[1 + start]
                stack_index = int(start / 4) + 1
                if item != ' ':
                    stacks[stack_index].insert(0, item)

    return (stacks, instructions)


def part_two(stacks, instructions):
    # print(stacks)
    for instruction in instructions:
        origin_stack = instruction[0]
        destination_stack = instruction[1]
        nb_items = instruction[2]
        items = stacks[origin_stack][-nb_items:]
        stacks[origin_stack] = stacks[origin_stack][:-nb_items]
        stacks[destination_stack] += items
        # print(instruction, "--->", stacks)

    top_items = ''
    for stack_index in range(1, 10):
        if len(stacks[stack_index]) >= 1:
            top_items += stacks[stack_index][-1]

    return top_items


if __name__ == "__main__":
    # ---- TEST DATA -----
    test_lines = [
        "    [D]    ",
        "[N] [C]    ",
        "[Z] [M] [P]",
        " 1   2   3 ",
        "",
        "move 1 from 2 to 1",
        "move 3 from 1 to 3",
        "move 2 from 2 to 1",
        "move 1 from 1 to 2"]
    print("-- Tests on test data:")
    test_stacks = {1: ["Z", "N"], 2: ["M", "C", "D"], 3: ["P"], 4: [], 5: [], 6: [], 7: [], 8: [], 9: []}
    test_instructions = [
        (2, 1),  # "move 1 from 2 to 1",
        (1, 3), (1, 3), (1, 3),  # "move 3 from 1 to 3",
        (2, 1), (2, 1),  # "move 2 from 2 to 1",
        (1, 2)  # "move 1 from 1 to 2"
    ]
    (stacks, instructions) = get_stacks_and_instructions(test_lines)
    print(stacks == test_stacks)
    print(instructions == test_instructions)
    print(part_one(stacks, instructions) == "CMZ")

    test_stacks_part_two = {1: ["Z", "N"], 2: ["M", "C", "D"], 3: ["P"], 4: [], 5: [], 6: [], 7: [], 8: [], 9: []}
    test_instructions_part_two = [
        (2, 1, 1),  # "move 1 from 2 to 1",
        (1, 3, 3),  # "move 3 from 1 to 3",
        (2, 1, 2),  # "move 2 from 2 to 1",
        (1, 2, 1)  # "move 1 from 1 to 2"
    ]
    (stacks_part_two, instructions_part_two) = get_stacks_and_instructions_part_two(test_lines)
    print(stacks_part_two == test_stacks_part_two)
    print(instructions_part_two == test_instructions_part_two)
    print(part_two(stacks_part_two, instructions_part_two) == "MCD")

    # ---- REAL DATA ----
    data = read_data("./2022/data/day05-input.txt")

    # Solution for 2-a
    print("\n-- Solution for 2-a:")
    (stacks, instructions) = get_stacks_and_instructions(data)
    print(part_one(stacks, instructions))

    # Solution for 2-b
    print("\n-- Solution for 2-b:")
    (stacks_part_two, instructions_part_two) = get_stacks_and_instructions_part_two(data)
    print(part_two(stacks_part_two, instructions_part_two))

# TODO: add complexity
