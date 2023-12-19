from collections import deque


def read_data(file_name):
    with open(file_name, 'r') as file:
        return [line.strip() for line in file.readlines()]


Direction = str
Depth = int
Color = str
Instruction = tuple[Direction, Depth, Color]
Position = tuple[int, int]
Lagoon = list[list[str]]


def parse_instructions(data: list[str]) -> list[Instruction]:
    instructions = []
    for line in data:
        direction, depth, color = line.split(" ")
        instructions.append((direction, int(depth), color))
    return instructions


DIRECTION = {
    "0": "R",
    "1": "D",
    "2": "L",
    "3": "U",
}


def parse_instructions_part_two(data: list[str]) -> list[Instruction]:
    instructions = []
    for line in data:
        _, _, color = line.split(" ")
        depth = int(color[2:7], 16)
        direction = DIRECTION[color[7]]
        instructions.append((direction, int(depth), color))
    return instructions


DELTAS = {
    "R": (0, 1),
    "L": (0, -1),
    "D": (1, 0),
    "U": (-1, 0),
}


def dig_trench(instructions: list[Instruction]) -> set[Position]:
    start = (0, 0)
    trench = {start}
    x, y = start
    for direction, depth, _ in instructions:
        delta = DELTAS[direction]
        for i in range(depth):
            x, y = x + delta[0], y + delta[1]
            trench.add((x, y))
    return trench


def create_lagoon(trench: set[Position]) -> Lagoon:
    max_x, max_y = max([x for x, y in trench]), max([y for x, y in trench])
    min_x, min_y = min([x for x, y in trench]), min([y for x, y in trench])
    lagoon = [['.' for _ in range(min_y, max_y + 1)] for _ in range(min_x, max_x + 1)]
    for x, y in trench:
        lagoon[x - min_x][y - min_y] = '#'
    return lagoon


def print_lagoon(lagoon: Lagoon):
    for line in lagoon:
        print("".join(line))


def get_neighbors(position: Position, lagoon: Lagoon) -> list[Position]:
    offsets = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    neighbors = []
    for offset in offsets:
        neighbor = (position[0] + offset[0], position[1] + offset[1])
        if 0 <= neighbor[0] < len(lagoon) and 0 <= neighbor[1] < len(lagoon[1]):
            neighbors.append(neighbor)
    return neighbors


def get_top_left_interior_point(lagoon: Lagoon) -> Position:
    i = 1
    inside = False
    for j in range(len(lagoon[0])):
        if inside:
            return i, j
        if lagoon[i][j] == "#":
            inside = True


def get_interior(lagoon: Lagoon) -> set[Position]:
    start = get_top_left_interior_point(lagoon)
    visited = set()
    to_visit = deque()  # queue
    to_visit.append(start)
    while len(to_visit) > 0:
        current = to_visit.popleft()
        if current in visited:
            continue
        visited.add(current)
        for neighbor in get_neighbors(current, lagoon):
            if lagoon[neighbor[0]][neighbor[1]] == "#":
                continue
            to_visit.append(neighbor)
    return visited


def part_one(data: list[str]) -> int:
    instructions = parse_instructions(data)
    trench = dig_trench(instructions)
    lagoon = create_lagoon(trench)
    # print_lagoon(lagoon)
    interior = get_interior(lagoon)
    return len(interior) + len(trench)


def shoelace_algorithm(instructions: list[Instruction]) -> int:
    # Get coordinates of edges
    coordinates = []
    coord = (0, 0)
    for direction, depth, _ in instructions:
        delta = DELTAS[direction]
        coord = (coord[0] + delta[0] * depth, coord[1] + delta[1] * depth)
        coordinates.append(coord)

    # Get total length of perimeter
    perimeter = 0
    for direction, depth, _ in instructions:
        perimeter += depth

    # Compute shoelace
    total = 0
    for c1, c2 in zip(coordinates, coordinates[1:] + [coordinates[0]]):
        total += (c1[1] + c2[1]) * (c2[0] - c1[0])

    return (abs(total) + perimeter) // 2 + 1


def part_two(data: list[str]) -> int:
    instructions = parse_instructions_part_two(data)
    result = shoelace_algorithm(instructions)
    return result


if __name__ == "__main__":
    # ---- TEST DATA -----
    test_data = [
        "R 6 (#70c710)",
        "D 5 (#0dc571)",
        "L 2 (#5713f0)",
        "D 2 (#d2c081)",
        "R 2 (#59c680)",
        "D 2 (#411b91)",
        "L 5 (#8ceee2)",
        "U 2 (#caa173)",
        "L 1 (#1b58a2)",
        "U 2 (#caa171)",
        "R 2 (#7807d2)",
        "U 3 (#a77fa3)",
        "L 2 (#015232)",
        "U 2 (#7a21e3)",
    ]
    print("-- Tests on test data:")
    print(part_one(test_data) == 62)
    print(part_two(test_data) == 952408144115)

    # ---- REAL DATA ----
    data = read_data("./2023/data/day18-input.txt")

    # Solution for part A
    print("\n-- Solution for part A:")
    print(part_one(data))  # 36807

    # Solution for part B
    print("\n-- Solution for part B:")
    print(part_two(data))  # 48797603984357
