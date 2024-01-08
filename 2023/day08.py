def read_data(file_name):
    with open(file_name, 'r') as file:
        return [line.strip() for line in file.readlines()]


class Node:
    def __init__(self, value: str):
        self.value = value
        self.left = None
        self.right = None

    def add_left(self, left):
        self.left = left

    def add_right(self, right):
        self.right = right

    def __repr__(self):
        return f"{self.value} --> ({self.left.value}, {self.right.value})"


def parse_data(data: list[str]):
    instruction = data[0]
    nodes = {}
    for line in data[2:]:
        value = line.split(" = (")[0]
        node = Node(value)
        nodes[value] = node

    for line in data[2:]:
        value = line.split(" = (")[0]
        left_value = line.split(" = (")[1].split(", ")[0]
        right_value = line.split(" = (")[1].split(", ")[1][:-1]
        node = nodes[value]
        left_node = nodes[left_value]
        right_node = nodes[right_value]
        node.add_left(left_node)
        node.add_right(right_node)

    return instruction, nodes


def part_one(data: list[str]) -> int:
    instructions, nodes = parse_data(data)

    i = 0
    node = nodes["AAA"]
    steps = 0
    while node.value != "ZZZ":
        steps += 1
        instruction = instructions[i]
        if instruction == "L":
            node = node.left
        elif instruction == "R":
            node = node.right
        i += 1
        if i >= len(instructions):
            i = 0

    return steps


def ends_with(value: str, letter: str) -> bool:
    return value[-1] == letter


def part_two_NON_OPTIM(data: list[str]) -> int:
    instructions, nodes = parse_data(data)

    current_nodes = [nodes[node] for node in nodes if ends_with(node, "A")]
    nb_nodes = len(current_nodes)
    i, steps = 0, 0
    while not len([node for node in current_nodes if ends_with(node.value, "Z")]) == nb_nodes:
        steps += 1
        instruction = instructions[i]
        for node_i in range(len(current_nodes)):
            node = current_nodes[node_i]
            if instruction == "L":
                current_nodes[node_i] = node.left
            elif instruction == "R":
                current_nodes[node_i] = node.right

        i += 1
        if i >= len(instructions):
            i = 0

    return steps


def count_steps(node, instructions):
    i = 0
    steps = 0
    while not ends_with(node.value, "Z"):
        steps += 1
        instruction = instructions[i]
        if instruction == "L":
            node = node.left
        elif instruction == "R":
            node = node.right
        i += 1
        if i >= len(instructions):
            i = 0

    return steps


def gcd(n, m):
    if m == 0:
        return n
    return gcd(m, n % m)


def compute_lcm(a: list[int]):
    lcm = 1
    for i in a:
        lcm = lcm * i // gcd(lcm, i)
    return lcm


def part_two(data: list[str]) -> int:
    instructions, nodes = parse_data(data)

    current_nodes = [nodes[node] for node in nodes if ends_with(node, "A")]
    steps = []
    for node in current_nodes:
        steps.append(count_steps(node, instructions))

    print(steps)
    return compute_lcm(steps)


if __name__ == "__main__":
    # ---- TEST DATA -----
    test_data_1 = [
        "RL",
        "",
        "AAA = (BBB, CCC)",
        "BBB = (DDD, EEE)",
        "CCC = (ZZZ, GGG)",
        "DDD = (DDD, DDD)",
        "EEE = (EEE, EEE)",
        "GGG = (GGG, GGG)",
        "ZZZ = (ZZZ, ZZZ)"
    ]
    test_data_2 = [
        "LLR",
        "",
        "AAA = (BBB, BBB)",
        "BBB = (AAA, ZZZ)",
        "ZZZ = (ZZZ, ZZZ)"
    ]
    test_data_3 = [
        "LR",
        "",
        "11A = (11B, XXX)",
        "11B = (XXX, 11Z)",
        "11Z = (11B, XXX)",
        "22A = (22B, XXX)",
        "22B = (22C, 22C)",
        "22C = (22Z, 22Z)",
        "22Z = (22B, 22B)",
        "XXX = (XXX, XXX)"
    ]
    print("-- Tests on test data:")
    print(part_one(test_data_1) == 2)
    print(part_one(test_data_2) == 6)
    print(part_two(test_data_3) == 6)

    # ---- REAL DATA ----
    data = read_data("./data/2023/day08-input.txt")

    # Solution for part A
    print("\n-- Solution for part A:")
    print(part_one(data))  # 19951

    # Solution for part B
    print("\n-- Solution for part B:")
    print(part_two(data))  # 16342438708751
