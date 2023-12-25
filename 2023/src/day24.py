from typing import Optional


def read_data(file_name):
    with open(file_name, 'r') as file:
        return file.read().strip()


Position = tuple[int, int, int]
Velocity = tuple[int, int, int]
Hailstone = tuple[Position, Velocity]


def parse_data(data: str) -> list[Hailstone]:
    hailstones = []
    for line in data.splitlines():
        raw_position, raw_velocity = line.split(" @ ")
        position = tuple([int(p) for p in raw_position.split(", ")])
        velocity = tuple([int(v) for v in raw_velocity.split(", ")])
        hailstones.append((position, velocity))
    return hailstones


def get_slope(hailstone: Hailstone) -> float:
    # Slope is dy/dx --> (y2 - y1) / (x2 - x1)
    position, velocity = hailstone
    x1, y1 = position[0], position[1]
    x2, y2 = position[0] + velocity[0], position[1] + velocity[1]
    return (y2 - y1) / (x2 - x1)


def get_y_intercept(hailstone: Hailstone, slope: float) -> float:
    #     y = ax + b
    # <-> b = y - ax
    position, _ = hailstone
    x, y, _ = position
    return y - slope * x


def find_intersection(h1: Hailstone, h2: Hailstone) -> Optional[tuple[float, float]]:
    h1_slope = get_slope(h1)
    h2_slope = get_slope(h2)
    h1_y_intercept = get_y_intercept(h1, h1_slope)
    h2_y_intercept = get_y_intercept(h2, h2_slope)

    if h1_slope == h2_slope:
        return None

    # The two slopes intersect at (x, y) if:
    #     a1 * x + b1 = a2 * x + b2
    # <-> (a1 - a2) * x = b2 - b1
    # <-> x = (b2 - b1) / (a1 - a2)
    x = (h2_y_intercept - h1_y_intercept) / (h1_slope - h2_slope)
    # y = ax + b (For any of the two)
    y = h1_slope * x + h1_y_intercept

    return x, y


def is_in_future_path(position: Position, hailstone: Hailstone):
    (x, y, _), (dx, dy, _) = hailstone
    # Check if (dx, dy) has same sign as (new_x - x, new_y - y)
    if (position[0] - x) / dx < 0:
        return False
    if (position[1] - y) / dy < 0:
        return False

    return True


def part_one(data: str, boundaries: tuple[tuple[int, int], tuple[int, int]]) -> int:
    hailstones = parse_data(data)
    x_min, x_max = boundaries[0]
    y_min, y_max = boundaries[1]

    nb_paths_crosses = 0
    all_pairs = [(h1, h2) for i, h1 in enumerate(hailstones) for h2 in hailstones[i + 1:]]
    for h1, h2 in all_pairs:
        intersection = find_intersection(h1, h2)
        # print(h1, h2, "-->", intersection)
        if intersection is None:
            continue
        x, y = intersection
        if not (x_min <= x <= x_max and y_min <= y <= y_max):
            continue
        if not is_in_future_path((x, y), h1):
            continue
        if not is_in_future_path((x, y), h2):
            continue
        nb_paths_crosses += 1

    return nb_paths_crosses


if __name__ == "__main__":
    # ---- TEST DATA -----
    test_data = r"""19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3"""
    print("-- Tests on test data:")
    boundaries = ((7, 27), (7, 27))
    print(part_one(test_data, boundaries) == 2)
    # print(part_two(test_data) == 154)

    # ---- REAL DATA ----
    data = read_data("./2023/data/day24-input.txt")

    # Solution for part A
    print("\n-- Solution for part A:")
    boundaries = ((200000000000000, 400000000000000), (200000000000000, 400000000000000))
    print(part_one(data, boundaries))  # 14046
    #
    # # Solution for part B
    # print("\n-- Solution for part B:")
    # print(part_two(data))  # 6450
