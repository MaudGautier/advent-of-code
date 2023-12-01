def read_data(file_name):
    with open(file_name, 'r') as file:
        return [line.strip() for line in file.readlines()]


def get_first_and_last_digits(calibration: str) -> tuple[str, str]:
    first_digit, last_digit = None, None
    for character in calibration:
        if not character.isdigit():
            continue

        last_digit = character

        if first_digit is None:
            first_digit = character

    return first_digit, last_digit


def combine_digits(first: str, last: str) -> int:
    return int(str(first) + str(last))


def part_one(calibrations):
    sum = 0
    for calibration in calibrations:
        first_digit, last_digit = get_first_and_last_digits(calibration)
        number = combine_digits(first_digit, last_digit)
        sum += number

    return sum


if __name__ == "__main__":
    # ---- TEST DATA -----
    test_data = [
        "1abc2",
        "pqr3stu8vwx",
        "a1b2c3d4e5f",
        "treb7uchet",
    ]
    print("-- Tests on test data:")
    print(part_one(test_data) == 142)

    # ---- REAL DATA ----
    data = read_data("./2023/data/day01-input.txt")

    # Solution for part A
    print("\n-- Solution for part A:")
    print(part_one(data))  #
