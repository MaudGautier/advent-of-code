from functools import cmp_to_key


def read_data_part_one(file_name):
    with open(file_name, 'r') as file:
        lines = [line.strip() for line in file.readlines()]
        pairs = []
        for i in range(len(lines) // 3 + 1):
            first_element = eval(lines[i * 3])
            second_element = eval(lines[i * 3 + 1])
            # empty_element = lines[I * 3 + 2]
            pairs.append((first_element, second_element))

        return pairs


def read_data_part_two(file_name):
    with open(file_name, 'r') as file:
        return [eval(line.strip()) for line in file.readlines() if line.strip()]


# Logique : Dès que un faux => return Faux, sinon, continue de checker le prochain
def is_in_correct_order(pair):
    first, second = pair
    # print("-- CHECKING", first, "VS", second)

    if type(first) == list and type(second) == list:
        len1 = len(first)
        len2 = len(second)

        for i in range(max(len1, len2)):
            # Deal with out of range cases
            if len1 != len2 and i == min(len1, len2):
                if len1 < len2:
                    return True
                else:
                    return False
            if first[i] == second[i]:
                # print("-- Are equal", first[i], "VS", second[i])
                continue
            return is_in_correct_order((first[i], second[i]))
        return True

    if type(first) == int and type(second) == int:
        if first < second:
            return True
        if first > second:
            return False
        # if first == second:
        # SHOULD NOT HAPPEN

    if type(first) == list and type(second) == int:
        return is_in_correct_order((first, [second]))
    if type(first) == int and type(second) == list:
        return is_in_correct_order(([first], second))

    print("Case not dealt with")
    return None


def part_one(pairs):
    pairs_correctly_ordered = []
    for pair_index, pair in enumerate(pairs):
        pair_id = pair_index + 1
        if is_in_correct_order(pair):
            # print("Pair", pair_id, "in correct order")
            pairs_correctly_ordered.append(pair_id)

    return sum(pairs_correctly_ordered)


def compare(item1, item2):
    if is_in_correct_order((item1, item2)):
        return -1
    elif not is_in_correct_order((item1, item2)):
        return 1
    else:
        return 0


def find_packet_id(packets, searched_packet):
    for packet_index, packet in enumerate(packets):
        packet_id = packet_index + 1
        if packet == searched_packet:
            return packet_id


def part_two(packets):
    divider_packet_1 = [[2]]
    divider_packet_2 = [[6]]

    packets.append(divider_packet_1)
    packets.append(divider_packet_2)

    sorted_packets = sorted(packets, key=cmp_to_key(compare))

    id_1 = find_packet_id(sorted_packets, divider_packet_1)
    id_2 = find_packet_id(sorted_packets, divider_packet_2)

    return id_1 * id_2


if __name__ == "__main__":
    # ---- TEST DATA -----
    test_data_1 = [
        ([1, 1, 3, 1, 1], [1, 1, 5, 1, 1]),
        ([[1], [2, 3, 4]], [[1], 4]),
        ([9], [[8, 7, 6]]),
        ([[4, 4], 4, 4], [[4, 4], 4, 4, 4]),
        ([7, 7, 7, 7], [7, 7, 7]),
        ([], [3]),
        ([[[]]], [[]]),
        ([1, [2, [3, [4, [5, 6, 7]]]], 8, 9], [1, [2, [3, [4, [5, 6, 0]]]], 8, 9])
    ]
    test_data_2 = [
        [1, 1, 3, 1, 1],
        [1, 1, 5, 1, 1],
        [[1], [2, 3, 4]],
        [[1], 4],
        [9],
        [[8, 7, 6]],
        [[4, 4], 4, 4],
        [[4, 4], 4, 4, 4],
        [7, 7, 7, 7],
        [7, 7, 7],
        [],
        [3],
        [[[]]],
        [[]],
        [1, [2, [3, [4, [5, 6, 7]]]], 8, 9],
        [1, [2, [3, [4, [5, 6, 0]]]], 8, 9]
    ]
    print("-- Tests on test data:")
    print(part_one(test_data_1) == 13)
    print(part_two(test_data_2) == 140)

    # ---- REAL DATA ----
    data_1 = read_data_part_one("./2022/data/day13-input.txt")
    data_2 = read_data_part_two("./2022/data/day13-input.txt")

    # Solution for part A
    print("\n-- Solution for part A:")
    print(part_one(data_1))  # 5675

    # Solution for part B
    print("\n-- Solution for part B:")
    print(part_two(data_2))  # 20383
