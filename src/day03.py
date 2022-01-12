#!/usr/bin/env python3
from typing import List, Dict, NamedTuple, Union, Callable

Rates = NamedTuple('Rates', (
    ('gamma_rate', int),
    ('epsilon_rate', int)
))


def count_zeros_and_ones(diagnostic_report: List[str]) -> Dict[int, List[int]]:
    counts = {}
    for binary in diagnostic_report:
        for index, digit in enumerate(binary):
            if not index in counts:
                counts[index] = [0, 0]
            counts[index][int(digit)] += 1

    # print(counts)
    return counts


def extract_most_common_bit(l: List[int]) -> Union[str, None]:
    if l[0] > l[1]:
        return "0"
    if l[0] < l[1]:
        return "1"
    return None


def extract_least_common_bit(l: List[int]) -> Union[str, None]:
    if l[0] > l[1]:
        return "1"
    if l[0] < l[1]:
        return "0"
    return None


def extract_bits(counts: Dict[int, List[int]], extract_function: Callable[[List[int]], Union[str, None]]) -> str:
    binary = ''
    for index, digit_counts in sorted(counts.items()):
        binary += extract_function(digit_counts)
    return binary


def transform_binary_to_decimal(binary: str) -> int:
    max_power = len(binary) - 1
    decimal = 0
    for index, digit in enumerate(binary):
        decimal += int(digit) * 2**(max_power-index)
    return decimal


def generate_diagnostics(diagnostic_report: List[str]) -> Rates:
    counts_per_position = count_zeros_and_ones(diagnostic_report)
    binary_gamma_rate = extract_bits(counts_per_position, extract_most_common_bit)
    binary_epsilon_rate = extract_bits(counts_per_position, extract_least_common_bit)
    gamma_rate = transform_binary_to_decimal(binary_gamma_rate)
    epsilon_rate = transform_binary_to_decimal(binary_epsilon_rate)
    return gamma_rate, epsilon_rate


def calculate_power_consumption(gamma_rate: int, epsilon_rate: int) -> int:
    return gamma_rate * epsilon_rate


def read_data(file_name: str) -> List[str]:
    with open(file_name, 'r') as file:
        return [binary.strip() for binary in file.readlines()]


if __name__== "__main__":
    # Check with test data
    test_data = ["00100",
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
                 "01010"]
    [gamma_rate, epsilon_rate] = generate_diagnostics(test_data)
    power_consumption = calculate_power_consumption(gamma_rate, epsilon_rate)
    print(gamma_rate == 22, epsilon_rate == 9, power_consumption == 9*22)

    # Solution for 3-a
    data = read_data('data/day03-input.txt')
    [gamma_rate, epsilon_rate] = generate_diagnostics(data)
    power_consumption = calculate_power_consumption(gamma_rate, epsilon_rate)
    print("Result for 3-a:", gamma_rate, epsilon_rate, "==", power_consumption)
