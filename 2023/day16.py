from collections import deque


def read_data(file_name):
    with open(file_name, 'r') as file:
        return file.read().strip()


Grid = list[list[str]]
Direction = str
Position = tuple[int, int]
Beam = tuple[Position, Direction]


def parse_grid(data: str) -> Grid:
    grid = []
    lines = data.split("\n")
    for line in lines:
        grid.append([char for char in line.strip()])
    return grid


def compute_new_position(position: Position, direction: Direction) -> Position:
    row, col = position
    if direction == "rightward":
        return row, col + 1
    if direction == "leftward":
        return row, col - 1
    if direction == "downward":
        return row + 1, col
    if direction == "upward":
        return row - 1, col
    raise ValueError("Direction not supported")


def is_valid(position: Position, grid: Grid) -> bool:
    (row, col) = position
    return 0 <= row < len(grid) and 0 <= col < len(grid[0])


def compute_new_beams(input_position: Position, direction: Direction, grid: Grid) -> list[Beam]:
    position = compute_new_position(input_position, direction)
    row, col = position
    if not is_valid((row, col), grid):
        return []

    # print("--- DEALING WITH", beam, ":", grid[beam[0]][beam[1]], "-> new pos", row, col, grid[row][col])

    # Empty
    if grid[row][col] == ".":
        return [(position, direction)]

    # Vertical split
    if grid[row][col] == "|" and direction in ["leftward", "rightward"]:
        return [(position, "upward"), (position, "downward")]
    if grid[row][col] == "|" and direction in ["upward", "downward"]:
        return [(position, direction)]

    # Horizontal split
    if grid[row][col] == "-" and direction in ["leftward", "rightward"]:
        return [(position, direction)]
    if grid[row][col] == "-" and direction in ["upward", "downward"]:
        return [(position, "leftward"), (position, "rightward")]

    # 90º - 1
    if grid[row][col] == "\\" and direction in ["leftward"]:
        return [(position, "upward")]
    if grid[row][col] == "\\" and direction in ["rightward"]:
        return [(position, "downward")]
    if grid[row][col] == "\\" and direction in ["upward"]:
        return [(position, "leftward")]
    if grid[row][col] == "\\" and direction in ["downward"]:
        return [(position, "rightward")]

    # 90º - 2
    if grid[row][col] == "/" and direction in ["leftward"]:
        return [(position, "downward")]
    if grid[row][col] == "/" and direction in ["rightward"]:
        return [(position, "upward")]
    if grid[row][col] == "/" and direction in ["upward"]:
        return [(position, "rightward")]
    if grid[row][col] == "/" and direction in ["downward"]:
        return [(position, "leftward")]

    raise ValueError("Case not handled in compute_new_beams")


def energize(grid: Grid, start: Beam = ((0, -1), "rightward")) -> Grid:
    energized_grid = [['.' for _ in line] for line in grid]

    beams = deque()  # queue
    beams.append(start)
    visited = set()
    while len(beams) > 0:
        position, direction = beams.popleft()
        if (position, direction) in visited:
            continue
        visited.add((position, direction))

        # Arbitrary convention: avoid case start
        if (position, direction) != start:
            energized_grid[position[0]][position[1]] = "#"

        new_beams = compute_new_beams(position, direction, grid)
        valid_new_beams = [beam for beam in new_beams if is_valid(beam[0], grid)]
        beams += valid_new_beams

    return energized_grid


def count_energized(grid: Grid) -> int:
    count = 0
    for line in grid:
        for char in line:
            if char == "#":
                count += 1
    return count


def part_one(data: str) -> int:
    grid = parse_grid(data)
    energized_grid = energize(grid)
    # for line in energized_grid:
    #     print("".join(line))
    return count_energized(energized_grid)


def define_all_starts(grid: Grid):
    starts = []
    for i in range(len(grid)):
        starts.append(((i, -1), "rightward"))
        starts.append(((i, len(grid)), "leftward"))
    for j in range(len(grid[0])):
        starts.append(((-1, j), "downward"))
        starts.append(((len(grid[0]), j), "upward"))
    return starts


def part_two(data: str) -> int:
    grid = parse_grid(data)
    starts = define_all_starts(grid)
    
    max_energy = 0
    for start in starts:
        energized_grid = energize(grid, start)
        energy = count_energized(energized_grid)
        max_energy = max(max_energy, energy)
    return max_energy


if __name__ == "__main__":
    # ---- TEST DATA -----
    test_data = r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|...."""
    test_data_2 = r"""\|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|...."""
    print("-- Tests on test data:")
    print(part_one(test_data) == 46)
    print(part_one(test_data_2) == 10)
    print(part_two(test_data) == 51)

    # ---- REAL DATA ----
    data = read_data("./data/2023/day16-input.txt")

    # Solution for part A
    print("\n-- Solution for part A:")
    print(part_one(data))  # 6605

    # Solution for part B
    print("\n-- Solution for part B:")
    print(part_two(data))  # 6766
    # NB: about 2 seconds to execute
