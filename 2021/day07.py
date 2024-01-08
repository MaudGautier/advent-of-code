#!/usr/bin/env python3
from typing import List

Position = int
Positions = List[int]
FuelAmount = int


def calculate_fuel_amount_to_reach_target(
    initial_positions: Positions, target: Position
) -> FuelAmount:
    fuel_amounts = [abs(target - p) for p in initial_positions]
    return sum(fuel_amounts)


def arithmetic_sum(max_value: int) -> int:
    return int((max_value + 1) * max_value / 2)


def calculate_non_linear_fuel_amount_to_reach_target(
    initial_positions: Positions, target: Position
) -> FuelAmount:
    fuel_amounts = [arithmetic_sum(abs(target - p)) for p in initial_positions]
    return sum(fuel_amounts)


def get_min_fuel(crab_positions: Positions, non_linear: bool = False) -> FuelAmount:
    fuel_amounts = []
    for target in range(min(crab_positions), max(crab_positions) + 1):
        if non_linear:
            fuel_amount = calculate_non_linear_fuel_amount_to_reach_target(
                crab_positions, target
            )
        else:
            fuel_amount = calculate_fuel_amount_to_reach_target(crab_positions, target)
        fuel_amounts.append(fuel_amount)

    return min(fuel_amounts)


def read_data(file_name: str) -> Positions:
    with open(file_name, "r") as file:
        return [int(p) for p in file.read().strip().split(",")]


if __name__ == "__main__":
    # Tests
    print("-- Tests on test data:")
    test_crab_positions = [16, 1, 2, 0, 4, 2, 7, 1, 2, 14]
    test_minimal_fuel = get_min_fuel(test_crab_positions)
    print(test_minimal_fuel == 37)
    test_minimal_fuel_non_linear = get_min_fuel(test_crab_positions, non_linear=True)
    print(test_minimal_fuel_non_linear == 168)

    # Solution for 7-a
    print("\n-- Solution for 7-a:")
    crab_positions = read_data("data/day07-input.txt")
    minimal_fuel = get_min_fuel(crab_positions)
    print("The minimal fuel amount for the selected position is:", minimal_fuel)

    # Solution for 7-b
    print("\n-- Solution for 7-b:")
    minimal_fuel_non_linear = get_min_fuel(crab_positions, non_linear=True)
    print(
        "The minimal fuel amount with non-linear calculus method for the selected position is:",
        minimal_fuel_non_linear,
    )  # 96708205
