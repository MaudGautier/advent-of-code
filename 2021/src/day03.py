#!/usr/bin/env python3
from typing import List, Dict, NamedTuple, Callable

Rates = NamedTuple(
    "Rates",
    (
        ("gamma_rate", int),
        ("epsilon_rate", int),
        ("oxygen_rate", int),
        ("co2_rate", int),
    ),
)


def count_zeros_and_ones(diagnostic_report: List[str]) -> Dict[int, List[int]]:
    counts = {}
    for binary in diagnostic_report:
        for index, digit in enumerate(binary):
            if index not in counts:
                counts[index] = [0, 0]
            counts[index][int(digit)] += 1

    return counts


def extract_most_common_bit(l: List[int]) -> str:
    if l[0] > l[1]:
        return "0"
    if l[0] <= l[1]:
        return "1"


def extract_least_common_bit(l: List[int]) -> str:
    if l[0] > l[1]:
        return "1"
    if l[0] <= l[1]:
        return "0"


def extract_bits(
    counts: Dict[int, List[int]], extract_function: Callable[[List[int]], str]
) -> str:
    binary = ""
    for index, digit_counts in sorted(counts.items()):
        binary += extract_function(digit_counts)
    return binary


def transform_binary_to_decimal(binary: str) -> int:
    max_power = len(binary) - 1
    decimal = 0
    for index, digit in enumerate(binary):
        decimal += int(digit) * 2 ** (max_power - index)
    return decimal


def subset_numbers(
    numbers: List[str], index: int, extract_function: Callable[[List[int]], str]
) -> List[str]:
    counts = count_zeros_and_ones(numbers)
    chosen_bit = extract_function(counts[index])
    selected_numbers = []
    for number in numbers:
        if number[index] == chosen_bit:
            selected_numbers.append(number)

    return selected_numbers


def extract_number(
    numbers: List[str], extract_function: Callable[[List[int]], str]
) -> str:
    remaining_numbers = numbers
    index = 0
    while len(remaining_numbers) > 1:
        remaining_numbers = subset_numbers(remaining_numbers, index, extract_function)
        index += 1

    return remaining_numbers[0]


def generate_diagnostics(diagnostic_report: List[str]) -> Rates:
    counts_per_position = count_zeros_and_ones(diagnostic_report)
    binary_gamma_rate = extract_bits(counts_per_position, extract_most_common_bit)
    binary_epsilon_rate = extract_bits(counts_per_position, extract_least_common_bit)
    binary_oxygen_rate = extract_number(diagnostic_report, extract_most_common_bit)
    binary_co2_rate = extract_number(diagnostic_report, extract_least_common_bit)
    gamma_rate = transform_binary_to_decimal(binary_gamma_rate)
    epsilon_rate = transform_binary_to_decimal(binary_epsilon_rate)
    oxygen_rate = transform_binary_to_decimal(binary_oxygen_rate)
    co2_rate = transform_binary_to_decimal(binary_co2_rate)
    return gamma_rate, epsilon_rate, oxygen_rate, co2_rate


def multiply(rate1: int, rate2: int) -> int:
    return rate1 * rate2


def read_data(file_name: str) -> List[str]:
    with open(file_name, "r") as file:
        return [binary.strip() for binary in file.readlines()]


if __name__ == "__main__":
    # Check with test data
    test_data = [
        "00100",
        "11110",
        "10110",
        "10111",
        "10101",
        "01111",
        "00111",
        "11100",
        "10000",
        "11001",
        "00010",
        "01010",
    ]
    (gamma_rate, epsilon_rate, oxygen_rate, co2_rate) = generate_diagnostics(test_data)
    power_consumption = multiply(gamma_rate, epsilon_rate)
    life_support_rating = multiply(oxygen_rate, co2_rate)
    print(gamma_rate == 22, epsilon_rate == 9, power_consumption == 9 * 22)
    print(oxygen_rate == 23, co2_rate == 10, life_support_rating == 23 * 10)

    # Solution for 3-a
    data = read_data("data/day03-input.txt")
    (gamma_rate, epsilon_rate, oxygen_rate, co2_rate) = generate_diagnostics(data)
    power_consumption = multiply(gamma_rate, epsilon_rate)
    life_support_rating = multiply(oxygen_rate, co2_rate)
    print("Result for 3-a:", gamma_rate, epsilon_rate, "==", power_consumption)
    print("Result for 3-b:", oxygen_rate, co2_rate, "==", life_support_rating)
