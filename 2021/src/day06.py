#!/usr/bin/env python3
from typing import List, Dict

Timer = int
Timers = List[Timer]
Count = int
TimerCounter = Dict[Timer, Count]


def initialize_fish_timers(file_name: str) -> Timers:
    with open(file_name, "r") as file:
        line = file.read().strip()
        return [int(timer) for timer in line.split(",")]


def get_timer_counter(timers: Timers) -> TimerCounter:
    timer_counts = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0}
    for timer in timers:
        timer_counts[timer] += 1

    return timer_counts


def update_timer_counter(timer_counter: TimerCounter):
    nb_fishes_to_add = timer_counter[0]
    for timer in range(1, 9):
        timer_counter[timer - 1] = timer_counter[timer]
    timer_counter[8] = nb_fishes_to_add
    timer_counter[6] = timer_counter[6] + nb_fishes_to_add

    return timer_counter


def count_fish(timers: Timers, nb_days: int) -> int:
    timer_counter = get_timer_counter(timers)
    for day in range(1, nb_days + 1):
        update_timer_counter(timer_counter)

    return sum(timer_counter.values())


if __name__ == "__main__":
    # Tests
    print("-- Tests on test data:")
    test_initial_fish_timers = [3, 4, 3, 1, 2]
    nb_test_fishes_after_18_days = count_fish(test_initial_fish_timers, 18)
    print(nb_test_fishes_after_18_days == 26)
    nb_test_fishes_after_80_days = count_fish(test_initial_fish_timers, 80)
    print(nb_test_fishes_after_80_days == 5934)
    nb_test_fishes_after_256_days = count_fish(test_initial_fish_timers, 256)
    print(nb_test_fishes_after_256_days == 26984457539)

    # Solution for 6-a
    print("\n-- Solution for 6-a:")
    initial_fish_timers = initialize_fish_timers("data/day06-input.txt")
    nb_fishes_after_80_days = count_fish(initial_fish_timers, 80)
    print("After 80 days, there are", nb_fishes_after_80_days, "fishes")  # 380243

    # Solution for 6-b
    print("\n-- Solution for 6-b:")
    nb_fishes_after_256_days = count_fish(initial_fish_timers, 256)
    print("After 256 days, there are", nb_fishes_after_256_days, "fishes")
