#!/usr/bin/env python3
from typing import List

Position = int
Positions = List[int]
FuelAmount = int


def calculate_fuel_amount_to_reach_position(
    initial_positions: Positions, target: Position
) -> FuelAmount:
    fuel_amounts = [abs(target - p) for p in initial_positions]
    return sum(fuel_amounts)


def get_min_fuel(crab_positions: Positions) -> FuelAmount:
    fuel_amounts = []
    for target in range(min(crab_positions), max(crab_positions) + 1):
        fuel_amount = calculate_fuel_amount_to_reach_position(crab_positions, target)
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

    # Solution for 7-a
    print("\n-- Solution for 7-a:")
    crab_positions = read_data("data/day07-input.txt")
    minimal_fuel = get_min_fuel(crab_positions)
    print("The minimal fuel amount for the selected position is:", minimal_fuel)
