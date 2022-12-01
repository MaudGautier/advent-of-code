#!/usr/bin/env python3
from typing import Union, List


# Data is formated as: ["4887", "9307", "", "5533", "7981", ...]
def read_data(file_name: str) -> List[str]:
    with open(file_name, "r") as file:
        return [line.strip() for line in file.readlines()]


def should_swith_to_next_elf(line: str) -> bool:
    return line == ""


def report_calories_in_inventory(elvish_inventory: List[int], calories: int):
    elvish_inventory.append(calories)


def initialize_calories_of_new_elf() -> int:
    return 0


# Output: elvish inventories of calories: [2000, 3000, 1000]
def create_elvish_inventories(data_lines: List[str]) -> List[int]:
    elvish_inventories = []
    calories_of_current_elf = initialize_calories_of_new_elf()
    for line in data_lines:
        if should_swith_to_next_elf(line):
            report_calories_in_inventory(elvish_inventories, calories_of_current_elf)
            calories_of_current_elf = initialize_calories_of_new_elf()
        else:
            calories_of_current_elf += int(line)
    return elvish_inventories


def compute_total_calories_of_top_elves(elvish_inventories: List[int], number_of_elves: int) -> int:
    elvish_inventories.sort(reverse=True)
    inventories_with_max_calories = elvish_inventories[0:number_of_elves]

    return sum(inventories_with_max_calories)


if __name__ == "__main__":
    # ---- TEST DATA -----
    test_data = [
        "1000", "2000", "3000", "",
        "4000", "",
        "5000", "6000", "",
        "7000", "8000", "9000", "",
        "10000", ""
    ]
    # Solution for 1-a & 1-b
    test_elvish_inventories = create_elvish_inventories(test_data)
    print(compute_total_calories_of_top_elves(test_elvish_inventories, 1))
    print(compute_total_calories_of_top_elves(test_elvish_inventories, 3))


    # ---- REAL DATA ----
    data = read_data("./2022/data/day01-input.txt")
    elvish_inventories = create_elvish_inventories(data)

    # Solution for 1-a
    print(compute_total_calories_of_top_elves(elvish_inventories, 1)) # 68802
    # Solution for 1-b
    print(compute_total_calories_of_top_elves(elvish_inventories, 3)) # 205370


# Algorithmic complexity:
# Time: o(n)  (with n: number of lines) (+ o(m log(m)) with m: number of inventories)
# Space: o(n) (array)