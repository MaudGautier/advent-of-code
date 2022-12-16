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
                False: f
            }
        return data


def part_one(data):
    number_inspected_items = {}
    for monkey in data:
        number_inspected_items[monkey] = 0

    for round in range(20):
        for monkey in data:
            decisions = data[monkey]
            items = decisions["items"]
            items_index_to_delete = []
            for item_index, item in enumerate(items):
                number_inspected_items[monkey] += 1
                worry_level = decisions["operation"](item)
                worry_level = math.floor(worry_level / 3)
                is_divisible = decisions["test_divisor"](worry_level)
                to_monkey = decisions[is_divisible]
                data[to_monkey]["items"].append(worry_level)
                items_index_to_delete.append(item_index)
                # print("Monkey", monkey, "inspects item", item, "-> to worry_level", worry_level, "--> throw to", to_monkey,
                #       "New items:", data[monkey]["items"], "other monkey items:", data[to_monkey]["items"])
            for item_index_to_delete in sorted(items_index_to_delete, reverse=True):
                data[monkey]["items"].pop(item_index_to_delete)
        # print("After round", round, "data:", data)

    print(number_inspected_items)
    most_inspected_numbers = sorted(number_inspected_items.values())
    return most_inspected_numbers[-2] * most_inspected_numbers[-1]


if __name__ == "__main__":
    # ---- TEST DATA -----
    test_data = read_data("./2022/data/day11-test-input.txt")
    # print(test_data)
    print("-- Tests on test data:")
    print(part_one(test_data) == 10605)
    # print(part_two(test_data) == ##)

    # # ---- REAL DATA ----
    data = read_data("./2022/data/day11-input.txt")

    # Solution for part A
    print("\n-- Solution for part A:")
    print(part_one(data))  # 151312
    #
    # # Solution for part B
    # print("\n-- Solution for part B:")
    # part_two(data)  # FCJAPJRE
