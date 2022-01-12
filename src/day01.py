#!/usr/bin/env python3
from typing import Union, List


def has_depth_increased(previous_depth: Union[int, type(None)], new_depth: int) -> bool:
    if previous_depth is None:
        return False
    return new_depth > previous_depth


def sum_depths(previous_n_depth: List[int], depth: int) -> Union[int, type(None)]:
    if None in previous_n_depth:
        return None
    return sum(previous_n_depth, depth)


def count_nb_increases(input_file: str, window_size: int) -> int:
    total_increases = 0
    previous_depth_sum = None
    previous_n_depths = [None]*(window_size-1)
    with open(input_file) as file:
        lines = file.readlines()
        for line in lines:
            depth = int(line.strip())
            depth_sum = sum_depths(previous_n_depths, depth)
            if has_depth_increased(previous_depth_sum, depth_sum):
                total_increases += 1
            previous_n_depths = (previous_n_depths + [depth])[1:]
            previous_depth_sum = depth_sum

    return total_increases


if __name__ == "__main__":
    print(count_nb_increases("data/day01-input.txt", 1) == 1184) # should still be 1184
    print(count_nb_increases("data/day01-input.txt", 3)) # 1158

