def read_data(file_name):
    with open(file_name, 'r') as file:
        return [line.strip() for line in file.readlines()]


def parse_sequences(data: list[str]):
    sequences = []
    for line in data:
        sequences.append([int(number) for number in line.split(" ")])

    return sequences


def compute_history_sequence(sequence: list[int]) -> list[int]:
    history = []
    for i in range(len(sequence) - 1):
        history.append(sequence[i + 1] - sequence[i])
    return history


def get_next_val(sequence: list[int]) -> int:
    history = [sequence]
    while not all(number == 0 for number in sequence):
        sequence = compute_history_sequence(sequence)
        history.append(sequence)

    for i in reversed(range(1, len(history))):
        next_val = history[i][-1] + history[i - 1][-1]
        history[i - 1].append(next_val)

    return history[0][-1]


def part_one(data: list[str]):
    sequences = parse_sequences(data)

    total = 0
    for sequence in sequences:
        next_val = get_next_val(sequence)
        total += next_val

    return total


if __name__ == "__main__":
    # ---- TEST DATA -----
    test_data = [
        "0 3 6 9 12 15",
        "1 3 6 10 15 21",
        "10 13 16 21 30 45"
    ]
    print("-- Tests on test data:")
    print(part_one(test_data) == 114)
    # print(part_two(test_data) == 6)

    # ---- REAL DATA ----
    data = read_data("./2023/data/day09-input.txt")

    # Solution for part A
    print("\n-- Solution for part A:")
    print(part_one(data))  # 1762065988
    #
    # # Solution for part B
    # print("\n-- Solution for part B:")
    # print(part_two(data))  # 16342438708751
