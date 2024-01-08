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


DIGITS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9
}


def get_first_and_last_digits_with_letters(calibration: str) -> tuple[str, str]:
    first_digit, last_digit = None, None
    for idx in range(len(calibration)):
        character = calibration[idx]
        # digit case
        if character.isdigit():
            if not character.isdigit():
                continue

            last_digit = character

            if first_digit is None:
                first_digit = character

            continue

        # letter case
        for digit_letter in DIGITS:
            if calibration[idx:idx + len(digit_letter)] != digit_letter:
                continue

            last_digit = str(DIGITS[digit_letter])

            if first_digit is None:
                first_digit = str(DIGITS[digit_letter])

    return first_digit, last_digit


def combine_digits(first: str, last: str) -> int:
    return int(str(first) + str(last))


def part_one(calibrations: list[str]) -> int:
    sum = 0
    for calibration in calibrations:
        first_digit, last_digit = get_first_and_last_digits(calibration)
        number = combine_digits(first_digit, last_digit)
        sum += number

    return sum


def part_two(calibrations: list[str]) -> int:
    sum = 0
    for calibration in calibrations:
        first_digit, last_digit = get_first_and_last_digits_with_letters(calibration)
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
    test_data_2 = [
        "two1nine",
        "eightwothree",
        "abcone2threexyz",
        "xtwone3four",
        "4nineeightseven2",
        "zoneight234",
        "7pqrstsixteen",
    ]
    print("-- Tests on test data:")
    print(part_one(test_data) == 142)
    print(part_two(test_data_2) == 281)

    # ---- REAL DATA ----
    data = read_data("./data/2023/day01-input.txt")

    # Solution for part A
    print("\n-- Solution for part A:")
    print(part_one(data))  # 54239

    # Solution for part B
    print("\n-- Solution for part B:")
    print(part_two(data))  # 55343
