def update_current_indexes(current_indexes, previous_index_of_number_moved, new_index_of_number_moved):
    new_current_indexes = current_indexes.copy()
    for id, current_index in enumerate(current_indexes):
        # print(id, current_index)
        if previous_index_of_number_moved < current_index and new_index_of_number_moved < current_index:
            # print("was before and remains before")
            tmp = "ok"
        elif previous_index_of_number_moved > current_index and new_index_of_number_moved > current_index:
            # print("was after and remains after")
            tmp = "ok"
        elif previous_index_of_number_moved < current_index and new_index_of_number_moved > current_index:
            # print("number moved was before and is now after => current number index has lost 1")
            new_current_indexes[id] = current_index - 1
        elif previous_index_of_number_moved > current_index and new_index_of_number_moved < current_index:
            # print("number moved was after and is now before => current number index has gained 1")
            new_current_indexes[id] = current_index + 1
        elif previous_index_of_number_moved == current_index:
            # print("the number moved is the current number checked => goes to its new position")
            new_current_indexes[id] = new_index_of_number_moved
        elif new_index_of_number_moved == current_index:
            # NB: probablement vrai parce qu'il était avant
            # print(
            #     "????? the number has been moved to the current number index checked => the current number goes to position - 1")
            new_current_indexes[id] = current_index - 1
        else:
            print("NOT DEALT", previous_index_of_number_moved, new_index_of_number_moved, current_index)

    return new_current_indexes


def part_one(sequence):
    original_sequence = sequence.copy()
    current_indexes = [i for i in range(len(sequence))]

    for i in range(len(original_sequence)):
        current_value = original_sequence[i]
        current_index = current_indexes[i]
        # print("\nDealing with", current_value, "at index", current_index, "in current_sequence", sequence)
        new_sequence = sequence[:current_index] + sequence[current_index + 1:]
        # print("with value cut", new_sequence)
        new_index = (current_index + current_value) % (len(sequence) - 1)  ## ???
        if new_index == 0:
            new_index = len(sequence) - 1
        new_new_sequence = new_sequence[: new_index] + [current_value] + new_sequence[new_index:]
        # print("NEW SEQ", new_new_sequence, "with", current_value, "at new index", new_index)
        sequence = new_new_sequence
        # Update current_indexes
        current_indexes = update_current_indexes(current_indexes, current_index, new_index)
        # print("new_current_indexes", current_indexes, "for original sequence", original_sequence)
        # print("????", current_indexes == [0, 1, 2, 4, 6, 3, 5])

    # print(new_new_sequence)
    id_0 = new_new_sequence.index(0)
    print("id_0", id_0)
    summed_value = 0
    for check in [1000, 2000, 3000]:
        summed_value += new_new_sequence[(id_0 + check) % 7]

    return summed_value
    # print(new_new_sequence[(id_0 + 1000) % 7])
    # print(new_new_sequence[(id_0 + 2000) % 7])
    # print(new_new_sequence[(id_0 + 3000) % 7])

    # i = 0
    # current_value = original_sequence[i]
    # current_index = current_indexes[i]
    # print("\nDealing with", current_value, "at index", current_index, "in current_sequence", sequence)
    # new_sequence = sequence[:current_index] + sequence[current_index + 1:]
    # print("with value cut", new_sequence)
    # new_index = (current_index + current_value) % (len(sequence) - 1)  ## ???
    # new_new_sequence = new_sequence[: new_index] + [current_value] + new_sequence[new_index:]
    # print("NEW SEQ", new_new_sequence, "with", current_value, "at new index", new_index)
    # sequence = new_new_sequence
    # # Update current_indexes
    # current_indexes = update_current_indexes(current_indexes, current_index, new_index)
    # print("new_current_indexes", current_indexes, "for original sequence", original_sequence)
    # print("????", current_indexes == [1, 0, 2, 3, 4, 5, 6])
    #
    # i = 1
    # current_value = original_sequence[i]
    # current_index = current_indexes[i]
    # print("\nDealing with", current_value, "at index", current_index, "in current_sequence", sequence)
    # new_sequence = sequence[:current_index] + sequence[current_index + 1:]
    # print("with value cut", new_sequence)
    # new_index = (current_index + current_value) % (len(sequence) - 1)  ## ???
    # new_new_sequence = new_sequence[: new_index] + [current_value] + new_sequence[new_index:]
    # print("NEW SEQ", new_new_sequence, "with", current_value, "at new index", new_index)
    # sequence = new_new_sequence
    # # Update current_indexes
    # current_indexes = update_current_indexes(current_indexes, current_index, new_index)
    # print("new_current_indexes", current_indexes, "for original sequence", original_sequence)
    # print("????", current_indexes == [0, 2, 1, 3, 4, 5, 6])
    #
    # i = 2
    # current_value = original_sequence[i]
    # current_index = current_indexes[i]
    # print("\nDealing with", current_value, "at index", current_index, "in current_sequence", sequence)
    # new_sequence = sequence[:current_index] + sequence[current_index + 1:]
    # print("with value cut", new_sequence)
    # new_index = (current_index + current_value) % (len(sequence) - 1)  ## ???
    # new_new_sequence = new_sequence[: new_index] + [current_value] + new_sequence[new_index:]
    # print("NEW SEQ", new_new_sequence, "with", current_value, "at new index", new_index)
    # sequence = new_new_sequence
    # # Update current_indexes
    # current_indexes = update_current_indexes(current_indexes, current_index, new_index)
    # print("new_current_indexes", current_indexes, "for original sequence", original_sequence)
    # print("????", current_indexes == [0, 1, 4, 2, 3, 5, 6])
    #
    # i = 3
    # current_value = original_sequence[i]
    # current_index = current_indexes[i]
    # print("\nDealing with", current_value, "at index", current_index, "in current_sequence", sequence)
    # new_sequence = sequence[:current_index] + sequence[current_index + 1:]
    # print("with value cut", new_sequence)
    # new_index = (current_index + current_value) % (len(sequence) - 1)  ## ???
    # new_new_sequence = new_sequence[: new_index] + [current_value] + new_sequence[new_index:]
    # print("NEW SEQ", new_new_sequence, "with", current_value, "at new index", new_index)
    # sequence = new_new_sequence
    # # Update current_indexes
    # current_indexes = update_current_indexes(current_indexes, current_index, new_index)
    # print("new_current_indexes", current_indexes, "for original sequence", original_sequence)
    # print("????", current_indexes == [0, 1, 3, 5, 2, 4, 6])
    #
    # i = 4
    # current_value = original_sequence[i]
    # current_index = current_indexes[i]
    # print("\nDealing with", current_value, "at index", current_index, "in current_sequence", sequence)
    # new_sequence = sequence[:current_index] + sequence[current_index + 1:]
    # print("with value cut", new_sequence)
    # new_index = (current_index + current_value) % (len(sequence) - 1)  ## ???
    # if new_index == 0:
    #     new_index = len(sequence) - 1
    # new_new_sequence = new_sequence[: new_index] + [current_value] + new_sequence[new_index:]
    # print("NEW SEQ", new_new_sequence, "with", current_value, "at new index", new_index)
    # sequence = new_new_sequence
    # # Update current_indexes
    # current_indexes = update_current_indexes(current_indexes, current_index, new_index)
    # print("new_current_indexes", current_indexes, "for original sequence", original_sequence)
    # print("????", current_indexes == [0, 1, 2, 4, 6, 3, 5])
    #
    # i = 5
    # current_value = original_sequence[i]
    # current_index = current_indexes[i]
    # print("\nDealing with", current_value, "at index", current_index, "in current_sequence", sequence)
    # new_sequence = sequence[:current_index] + sequence[current_index + 1:]
    # print("with value cut", new_sequence)
    # new_index = (current_index + current_value) % (len(sequence) - 1)  ## ???
    # if new_index == 0:
    #     new_index = len(sequence) - 1
    # new_new_sequence = new_sequence[: new_index] + [current_value] + new_sequence[new_index:]
    # print("NEW SEQ", new_new_sequence, "with", current_value, "at new index", new_index)
    # sequence = new_new_sequence
    # # Update current_indexes
    # current_indexes = update_current_indexes(current_indexes, current_index, new_index)
    # print("new_current_indexes", current_indexes, "for original sequence", original_sequence)
    # print("????", current_indexes == [0, 1, 2, 4, 6, 3, 5])
    #
    # i = 6
    # current_value = original_sequence[i]
    # current_index = current_indexes[i]
    # print("\nDealing with", current_value, "at index", current_index, "in current_sequence", sequence)
    # new_sequence = sequence[:current_index] + sequence[current_index + 1:]
    # print("with value cut", new_sequence)
    # new_index = (current_index + current_value) % (len(sequence) - 1)  ## ???
    # if new_index == 0:
    #     new_index = len(sequence) - 1
    # new_new_sequence = new_sequence[: new_index] + [current_value] + new_sequence[new_index:]
    # print("NEW SEQ", new_new_sequence, "with", current_value, "at new index", new_index)
    # sequence = new_new_sequence
    # # Update current_indexes
    # current_indexes = update_current_indexes(current_indexes, current_index, new_index)
    # print("new_current_indexes", current_indexes, "for original sequence", original_sequence)
    # print("????", current_indexes == [0, 1, 2, 4, 6, 3, 5])


def read_data(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()
        return [int(line.strip()) for line in lines]


if __name__ == "__main__":
    # ---- TEST DATA -----
    test_data = [
        1,
        2,
        -3,
        3,
        -2,
        0,
        4,
    ]
    print("-- Tests on test data:")
    print(part_one(test_data) == 3)

    # # ---- REAL DATA ----
    # data = read_data("./2022/data/day20-input.txt")
    # print(data)
    #
    # # Solution for part A
    # print("\n-- Solution for part A:")
    # print(part_one(data))  # -4651 INCORRECT
