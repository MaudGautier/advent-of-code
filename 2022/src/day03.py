from typing import List, Tuple, Literal, Dict, Type, Union

CompartmentOne = str
CompartmentTwo = str
Items = str


# Output: [("A", "X"), ("B", "Y"), ("C", "Z")]
def read_data(file_name: str) -> List[str]:
    with open(file_name, 'r') as file:
        return [line.strip() for line in file.readlines()]


def divide_items_into_compartments(items: Items) -> Tuple[CompartmentOne, CompartmentTwo]:
    # Assuming all lines have even length. Else, will throw error later
    nb_items_in_each_compartment = int(len(items) / 2)
    compartment_one = items[0:nb_items_in_each_compartment]
    compartment_two = items[nb_items_in_each_compartment:]
    return compartment_one, compartment_two


def find_faulty_item(compartment_one: CompartmentOne, compartment_two: CompartmentTwo) -> str:
    for item in compartment_one:
        if item in compartment_two:
            return item


def get_priority(item: str) -> int:
    ascii_value = ord(item)
    # Is A -> Z
    if 65 <= ascii_value <= 90:
        return ascii_value - 65 + 27
    if 97 <= ascii_value <= 122:
        return ascii_value - 97 + 1


def part_one(items_list: Items) -> int:
    summed_priority = 0
    for items in items_list:
        (compartment_one, compartment_two) = divide_items_into_compartments(items)
        faulty_item = find_faulty_item(compartment_one, compartment_two)
        summed_priority += get_priority(faulty_item)

    return summed_priority


if __name__ == "__main__":
    # ---- TEST DATA -----
    test_data = [
        "vJrwpWtwJgWrhcsFMMfFFhFp",
        "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL",
        "PmmdzqPrVvPwwTWBwg",
        "wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn",
        "ttgJtRGJQctTZtZT",
        "CrZsJsPPZsGzwwsLwLmpwMDw"
    ]
    print("-- Tests on test data:")
    print(part_one(test_data) == 157)

    # ---- REAL DATA ----
    data = read_data("./2022/data/day03-input.txt")

    # Solution for 2-a
    print("\n-- Solution for 2-a:")
    print(part_one(data))

    # Solution for 2-b
    print("\n-- Solution for 2-b:")

# TODO: add complexity
