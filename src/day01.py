from typing import Union


def has_depth_increased(previous_depth: Union[int, type(None)], new_depth: int) -> bool:
    if previous_depth is None:
        return False
    return new_depth > previous_depth


def count_nb_increases(input_file: str) -> int:
    total_increases = 0
    previous_depth = None
    with open(input_file) as file:
        lines = file.readlines()
        for line in lines:
            depth = int(line.strip())
            if has_depth_increased(previous_depth, depth):
                total_increases += 1
            previous_depth = depth

    return total_increases


if __name__ == "__main__":
    print(count_nb_increases("data/day01-input.txt"))

