def read_data(file_name):
    with open(file_name, 'r') as file:
        return [line.strip() for line in file.readlines()]


def get_full_number(data, row, col_start):
    number = ""
    col = col_start
    while col < len(data[row]) and data[row][col].isdigit():
        number += data[row][col]
        col += 1

    return int(number), col


def get_numbers_and_symbols(data: list[str]):
    numbers = {}
    symbols = {}
    for row_idx, row in enumerate(data):
        col_idx = 0
        while col_idx < len(row):
            cell = data[row_idx][col_idx]
            if cell == ".":
                col_idx += 1
                continue

            if cell.isdigit():
                col_start = col_idx
                number, col_idx = get_full_number(data, row_idx, col_idx)
                for col in range(col_start, col_idx):
                    numbers[(row_idx, col)] = number, [col_start, col_idx]
                continue

            symbols[cell] = symbols.get(cell, []) + [(row_idx, col_idx)]

            col_idx += 1

    return numbers, symbols


def get_neighbors(position):
    row, col = position
    adjacents = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1), (0, 0), (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]
    return [(row + adjacent[0], col + adjacent[1]) for adjacent in adjacents]


def part_one(data: list[str]):
    numbers, symbols = get_numbers_and_symbols(data)

    total = 0
    seen = set()
    for symbol, positions in symbols.items():
        for position in positions:
            neighbors = get_neighbors(position)
            for neighbor in neighbors:
                if data[neighbor[0]][neighbor[1]].isdigit():
                    if (neighbor[0], neighbor[1]) in seen:
                        continue
                    number, cols = numbers[(neighbor[0], neighbor[1])]
                    total += number
                    for col in range(cols[0], cols[1]):
                        seen.add((neighbor[0], col))

    return total


def find_gear_parts(position, numbers, data):
    seen = set()
    gear_parts = []
    neighbors = get_neighbors(position)
    for neighbor in neighbors:
        if data[neighbor[0]][neighbor[1]].isdigit():
            if (neighbor[0], neighbor[1]) in seen:
                continue
            number, cols = numbers[(neighbor[0], neighbor[1])]
            gear_parts.append(number)
            for col in range(cols[0], cols[1]):
                seen.add((neighbor[0], col))

    return gear_parts


def multiply_gears(symbols, numbers, data):
    total = 0
    for position in symbols["*"]:
        gear_parts = find_gear_parts(position, numbers, data)
        if len(gear_parts) == 2:
            gear_ratio = gear_parts[0] * gear_parts[1]
            total += gear_ratio

    return total


def part_two(data: list[str]):
    numbers, symbols = get_numbers_and_symbols(data)
    return multiply_gears(symbols, numbers, data)


if __name__ == "__main__":
    # ---- TEST DATA -----
    test_data = [
        "467..114..",
        "...*......",
        "..35..633.",
        "......#...",
        "617*......",
        ".....+.58.",
        "..592.....",
        "......755.",
        "...$.*....",
        ".664.598..",
    ]
    print("-- Tests on test data:")
    print(part_one(test_data) == 4361)
    print(part_two(test_data) == 467835)

    # ---- REAL DATA ----
    data = read_data("./data/2023/day03-input.txt")

    # Solution for part A
    print("\n-- Solution for part A:")
    print(part_one(data))  # 529618

    # Solution for part B
    print("\n-- Solution for part B:")
    print(part_two(data))  # 77509019
