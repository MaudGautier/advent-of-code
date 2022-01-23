#!/usr/bin/env python3
from typing import List, NamedTuple

Timers = List[int]


def initialize_fish_timers(file_name: str) -> Timers:
    with open(file_name, "r") as file:
        line = file.read().strip()
        return [int(timer) for timer in line.split(",")]


def update_timers(timers: Timers):
    nb_new_timers = 0
    for timer_index, timer in enumerate(timers):
        if timer == 0:
            timers[timer_index] = 6
            nb_new_timers += 1
        else:
            timers[timer_index] -= 1

    timers.extend([8] * nb_new_timers)


def count_fish(timers: Timers, nb_days: int) -> int:
    # Only copy list of timers to avoid mistakes if reusing the same input list on several tests
    timers = timers.copy()
    for day in range(nb_days):
        update_timers(timers)

    return len(timers)


if __name__ == "__main__":
    # Tests
    print("-- Tests on test data:")
    test_initial_fish_timers = [3, 4, 3, 1, 2]
    nb_test_fishes_after_18_days = count_fish(test_initial_fish_timers, 18)
    print(nb_test_fishes_after_18_days == 26)
    nb_test_fishes_after_80_days = count_fish(test_initial_fish_timers, 80)
    print(nb_test_fishes_after_80_days == 5934)

    # Solution for 6-a
    print("\n-- Solution for 6-a:")
    initial_fish_timers = initialize_fish_timers("data/day06-input.txt")
    nb_fishes_after_80_days = count_fish(initial_fish_timers, 80)
    print("After 80 days, there are", nb_fishes_after_80_days, "fishes")  # 380243
