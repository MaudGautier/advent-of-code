def read_data(file_name):
    with open(file_name, 'r') as file:
        return file.readlines()[0].strip()


def all_characters_differ(sequence, sequence_length):
    return len(set(list(sequence))) == sequence_length


def get_sequence_marker_index(signal, sequence_length):
    for sequence_start in range(len(signal) - sequence_length):
        sequence = signal[sequence_start:sequence_start + sequence_length]
        if all_characters_differ(sequence, sequence_length):
            return sequence_start + sequence_length


def part_one(signal):
    sequence_length = 4
    return get_sequence_marker_index(signal, sequence_length)


def part_two(signal):
    sequence_length = 14
    return get_sequence_marker_index(signal, sequence_length)


if __name__ == "__main__":
    # ---- TEST DATA -----
    test_data_1 = "mjqjpqmgbljsphdztnvjfqwrcgsmlb"
    test_data_2 = "bvwbjplbgvbhsrlpgdmjqwftvncz"
    test_data_3 = "nppdvjthqldpwncqszvftbrmjlhg"
    test_data_4 = "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg"
    test_data_5 = "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"
    print("-- Tests on test data:")
    print("-- - for part 1:")
    print(part_one(test_data_1) == 7)
    print(part_one(test_data_2) == 5)
    print(part_one(test_data_3) == 6)
    print(part_one(test_data_4) == 10)
    print(part_one(test_data_5) == 11)
    print("-- - for part 2:")
    print(part_two(test_data_1) == 19)
    print(part_two(test_data_2) == 23)
    print(part_two(test_data_3) == 23)
    print(part_two(test_data_4) == 29)
    print(part_two(test_data_5) == 26)

    # ---- REAL DATA ----
    data = read_data("./2022/data/day06-input.txt")

    # Solution for 2-a
    print("\n-- Solution for 2-a:")
    print(part_one(data))

    # Solution for 2-b
    print("\n-- Solution for 2-b:")
    print(part_two(data))

# TODO: add complexity
