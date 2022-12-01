#!/usr/bin/env python3
from typing import Union, List


# Output: list of bag calories: [2000, 3000, 1000]
def extract_elves_bags(input_file: str) -> List[int]:
    with open(input_file) as file:
        lines = file.readlines()
        elves_bags = []
        current_bag = 0
        for line in lines:
            if line == "\n":
                elves_bags.append(current_bag)
                current_bag = 0
            else:
                current_bag += int(line.strip())
    return elves_bags


def select_max_calories(elves_bags: List[int]) -> int:
    max_calories = 0
    for bag in elves_bags:
        if bag >= max_calories:
            max_calories = bag

    return max_calories


def select_biggest_calories_bag(input_file: str) -> int:
    elves_bags = extract_elves_bags(input_file)
    return select_max_calories(elves_bags)


if __name__ == "__main__":
    print(select_biggest_calories_bag("./2022/data/day01-input.txt"))
