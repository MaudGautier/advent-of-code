def read_data(file_name):
    with open(file_name, 'r') as file:
        return file.read().strip()


Position = tuple[int, int, int]
Brick = tuple[Position, Position]


def parse_bricks(data: str) -> list[Brick]:
    bricks = []
    for line in data.splitlines():
        s, e = line.split("~")
        start = tuple([int(a) for a in s.split(",")])
        end = tuple([int(a) for a in e.split(",")])
        bricks.append((start, end))
    sorted_bricks = sorted(bricks, key=lambda x: min(x[0][2], x[1][2]))
    return sorted_bricks


def get_cubes(brick: Brick) -> list[Position]:
    start, end = brick
    if start == end:
        return [start]
    x_start, x_end = min(start[0], end[0]), max(start[0], end[0])
    y_start, y_end = min(start[1], end[1]), max(start[1], end[1])
    z_start, z_end = min(start[2], end[2]), max(start[2], end[2])
    if x_start != x_end:
        return [(x, y_start, z_start) for x in range(x_start, x_end + 1)]
    if y_start != y_end:
        return [(x_start, y, z_start) for y in range(y_start, y_end + 1)]
    if z_start != z_end:
        return [(x_start, y_start, z) for z in range(z_start, z_end + 1)]
    raise ValueError("2 coordinates differ. This should not happen!", brick)


def drop_brick(brick: Brick, filled_spaces: set[Position]) -> Brick:
    while True:
        cubes = get_cubes(brick)
        can_go_down = all([(cube[0], cube[1], cube[2] - 1) not in filled_spaces and cube[2] != 1 for cube in cubes])
        # print(brick, cubes, can_go_down)
        if not can_go_down:
            return brick
        start, end = brick
        brick = ((start[0], start[1], start[2] - 1), (end[0], end[1], end[2] - 1))
        # print("new brick", brick)


def drop(bricks: list[Brick]) -> list[Brick]:
    settled_bricks = []
    filled_spaces = set()
    for brick in bricks:
        dropped_brick = drop_brick(brick, filled_spaces)
        for cube in get_cubes(dropped_brick):
            filled_spaces.add(cube)
        settled_bricks.append(dropped_brick)

    return settled_bricks


def part_one(data: str) -> int:
    bricks = parse_bricks(data)

    # Settle all bricks
    settled_bricks = drop(bricks)

    # Try to remove one and increment count if the newly settled bricks remain identical
    nb_disintegratable = 0
    for i in range(len(settled_bricks)):
        # removed_brick = settled_bricks[i]
        settled_bricks_without_removed = settled_bricks[:i] + settled_bricks[i + 1:]
        new_settled_bricks_without_removed = drop(settled_bricks_without_removed)
        if settled_bricks_without_removed == new_settled_bricks_without_removed:
            nb_disintegratable += 1

    return nb_disintegratable


def part_two(data: str) -> int:
    bricks = parse_bricks(data)

    # Settle all bricks
    settled_bricks = drop(bricks)

    # Try to remove one and increment count for each newly settled bricks that falls
    nb_falls = 0
    for i in range(len(settled_bricks)):
        # removed_brick = settled_bricks[i]
        settled_bricks_without_removed = settled_bricks[:i] + settled_bricks[i + 1:]
        new_settled_bricks_without_removed = drop(settled_bricks_without_removed)
        for b1, b2 in zip(settled_bricks_without_removed, new_settled_bricks_without_removed):
            if b1 != b2:
                nb_falls += 1

    return nb_falls


if __name__ == "__main__":
    # ---- TEST DATA -----
    test_data = r"""1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9"""
    print("-- Tests on test data:")
    print(part_one(test_data) == 5)
    print(part_two(test_data) == 7)

    # ---- REAL DATA ----
    data = read_data("./2023/data/day22-input.txt")

    # Solution for part A
    print("\n-- Solution for part A:")
    print(part_one(data))  # 405
    # About 5 seconds to execute

    # Solution for part B
    print("\n-- Solution for part B:")
    print(part_two(data))  # 61297
    # About 5 seconds to execute
