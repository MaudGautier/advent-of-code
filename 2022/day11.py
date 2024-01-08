import math


def read_data(file_name):
    with open(file_name, 'r') as file:
        monkeys = [monkey.split("\n") for monkey in file.read().strip().split("\n\n")]
        data = {}
        for monkey in monkeys:
            key = int(monkey[0].split(" ")[1].split(":")[0])
            items = [int(item) for item in monkey[1].split(": ")[1].split(", ")]
            operation = eval("lambda old: o" + monkey[2].strip("Operation: new ="))
            divisor = int(monkey[3].strip("Test: divisible by"))
            test_divisor = eval("lambda x: x % " + str(divisor) + " == 0")
            t = int(monkey[4].strip("If true: throw to monkey "))
            f = int(monkey[5].strip("If false: throw to monkey "))

            data[key] = {
                "items": items,
                "operation": operation,
                "test_divisor": test_divisor,
                True: t,
                False: f,
                "divisor": divisor,
            }
        return data


def run_one_round(monkeys, number_inspected_items, worry_level_manager):
    for monkey in monkeys:
        decisions = monkeys[monkey]
        items = decisions["items"]
        items_index_to_delete = []
        for item_index, item in enumerate(items):
            number_inspected_items[monkey] += 1
            worry_level = decisions["operation"](item)
            worry_level = worry_level_manager(worry_level)
            is_divisible = decisions["test_divisor"](worry_level)
            to_monkey = decisions[is_divisible]
            monkeys[to_monkey]["items"].append(worry_level)
            items_index_to_delete.append(item_index)
        for item_index_to_delete in sorted(items_index_to_delete, reverse=True):
            monkeys[monkey]["items"].pop(item_index_to_delete)
        # print("Monkey", monkey, "inspected", number_inspected_items[monkey], "items")


def part_one(monkeys):
    number_inspected_items = {}
    for monkey in monkeys:
        number_inspected_items[monkey] = 0

    worry_level_manager = (lambda x: math.floor(x / 3))

    for round in range(20):
        # print("== After round", round + 1, "==")
        run_one_round(monkeys, number_inspected_items, worry_level_manager)

    most_inspected_numbers = sorted(number_inspected_items.values())
    return most_inspected_numbers[-2] * most_inspected_numbers[-1]


def compute_least_common_multiplier(monkeys):
    least_common_multiplier = 1
    for monkey in monkeys:
        least_common_multiplier *= monkeys[monkey]["divisor"]

    return least_common_multiplier


def part_two(monkeys):
    number_inspected_items = {}
    for monkey in monkeys:
        number_inspected_items[monkey] = 0

    least_common_multiplier = compute_least_common_multiplier(monkeys)
    worry_level_manager = (lambda x: x % least_common_multiplier)

    for round in range(10000):
        # print("== After round", round + 1, "==")
        run_one_round(monkeys, number_inspected_items, worry_level_manager)

    most_inspected_numbers = sorted(number_inspected_items.values())
    return most_inspected_numbers[-2] * most_inspected_numbers[-1]


if __name__ == "__main__":
    # ---- TEST DATA -----
    test_data_1 = read_data("./2022/data/day11-test-input.txt")
    test_data_2 = read_data("./2022/data/day11-test-input.txt")  # because test_data_1 has been mutated
    print("-- Tests on test data:")
    print(part_one(test_data_1) == 10605)
    print(part_two(test_data_2) == 2713310158)

    # ---- REAL DATA ----
    data_1 = read_data("./2022/data/day11-input.txt")
    data_2 = read_data("./2022/data/day11-input.txt")  # because data_1 has been mutated

    # Solution for part A
    print("\n-- Solution for part A:")
    print(part_one(data_1))  # 151312

    # Solution for part B
    print("\n-- Solution for part B:")
    print(part_two(data_2))  # 51382025916
