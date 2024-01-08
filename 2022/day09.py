def read_data(file_name):
    with open(file_name, 'r') as file:
        lines = [line.strip().split(" ") for line in file.readlines()]
        return [(direction, int(steps)) for [direction, steps] in lines]


def compute_new_head_position(position, direction):
    row = position[0]
    col = position[1]
    if direction == "R":
        return (row, col + 1)
    if direction == "L":
        return (row, col - 1)
    if direction == "U":
        return (row + 1, col)
    if direction == "D":
        return (row - 1, col)


def compute_new_tail_position(head_position, tail_position):
    head_row = head_position[0]
    head_col = head_position[1]
    tail_row = tail_position[0]
    tail_col = tail_position[1]

    # Already touching => no need to move
    if -1 <= head_row - tail_row <= 1 and -1 <= head_col - tail_col <= 1:
        return tail_position

    # Need move right
    if head_row == tail_row and head_col > tail_col + 1:
        return (tail_row, tail_col + 1)

    # Need move diagonal up right
    if head_row >= tail_row + 1 and head_col >= tail_col + 1:
        return (tail_row + 1, tail_col + 1)

    # Need move up
    if head_row > tail_row + 1 and head_col == tail_col:
        return (tail_row + 1, tail_col)

    # Need move diagonal up left
    if head_row >= tail_row + 1 and head_col <= tail_col - 1:
        return (tail_row + 1, tail_col - 1)

    # Need move left
    if head_row == tail_row and head_col < tail_col - 1:
        return (tail_row, tail_col - 1)

    # Need move diagonal down right
    if head_row <= tail_row - 1 and head_col >= tail_col + 1:
        return (tail_row - 1, tail_col + 1)

    # Need move diagonal down left
    if head_row <= tail_row - 1 and head_col <= tail_col - 1:
        return (tail_row - 1, tail_col - 1)

    # Need move down
    if head_row < tail_row - 1 and head_col == tail_col:
        return (tail_row - 1, tail_col)


def part_one(motions):
    list_tail_positions = [(0, 0)]
    current_head_position = (0, 0)
    for motion in motions:
        direction = motion[0]
        steps = motion[1]
        for step in range(steps):
            current_tail_position = list_tail_positions[-1]
            # print("------ For direction", direction, "STEP", step)
            # print("Current H", current_head_position, "Current T", current_tail_position)
            current_head_position = compute_new_head_position(current_head_position, direction)
            new_tail_position = compute_new_tail_position(current_head_position, current_tail_position)
            list_tail_positions.append(new_tail_position)
            # print("New H", current_head_position, "New T", new_tail_position)

    return len(set(list_tail_positions))


def part_two(motions):
    rope_positions = {
        0: [(0, 0)],
        1: [(0, 0)],
        2: [(0, 0)],
        3: [(0, 0)],
        4: [(0, 0)],
        5: [(0, 0)],
        6: [(0, 0)],
        7: [(0, 0)],
        8: [(0, 0)],
        9: [(0, 0)],
    }

    for motion in motions:
        direction = motion[0]
        steps = motion[1]
        # print("------ For direction", direction)
        for step in range(steps):
            for rope in rope_positions:
                if rope == 0:
                    current_head_position = rope_positions[rope][-1]
                    current_head_position = compute_new_head_position(current_head_position, direction)
                    rope_positions[rope].append(current_head_position)
                else:
                    current_tail_position = rope_positions[rope][-1]
                    current_head_position = rope_positions[rope - 1][-1]
                    new_tail_position = compute_new_tail_position(current_head_position, current_tail_position)
                    rope_positions[rope].append(new_tail_position)

        # print("end rope positions", rope_positions)

    return len(set(rope_positions[9]))


if __name__ == "__main__":
    # ---- TEST DATA -----
    test_data = [
        ("R", 4),
        ("U", 4),
        ("L", 3),
        ("D", 1),
        ("R", 4),
        ("D", 1),
        ("L", 5),
        ("R", 2),
    ]
    test_data_2 = [
        ("R", 5),
        ("U", 8),
        ("L", 8),
        ("D", 3),
        ("R", 17),
        ("D", 10),
        ("L", 25),
        ("U", 20),
    ]
    print("-- Tests on test data:")
    print(part_one(test_data) == 13)
    print(part_two(test_data) == 1)
    print(part_two(test_data_2) == 36)

    # ---- REAL DATA ----
    data = read_data("./2022/data/day09-input.txt")

    # Solution for part A
    print("\n-- Solution for part A:")
    print(part_one(data))  # 5695

    # Solution for part B
    print("\n-- Solution for part B:")
    print(part_two(data))  # 2434
