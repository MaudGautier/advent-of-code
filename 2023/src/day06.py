def read_data(file_name):
    with open(file_name, 'r') as file:
        return tuple([line.strip() for line in file.readlines()])


def parse_races(data: tuple[str, str]) -> list[tuple[int, int]]:
    times = [int(time) for time in data[0].split(":")[1].split()]
    distances = [int(distance) for distance in data[1].split(":")[1].split()]

    return list(zip(times, distances))


def compute_number_ways_to_win(race: tuple[int, int]) -> int:
    for i in range(race[0]):
        time, distance = race
        distance_achieved = (time - i) * i
        if distance_achieved > distance:
            mini = i
            break
    for i in reversed(range(race[0])):
        time, distance = race
        distance_achieved = (time - i) * i
        if distance_achieved > distance:
            maxi = i
            break

    return maxi - mini + 1



def part_one(data: tuple[str, str]) -> int:
    races = parse_races(data)
    total = 1
    for race in races:
        nb_ways = compute_number_ways_to_win(race)
        total *= nb_ways
    return total


if __name__ == "__main__":
    # ---- TEST DATA -----
    test_data = (
        "Time:      7  15   30",
        "Distance:  9  40  200",
    )
    print("-- Tests on test data:")
    print(part_one(test_data) == 288)
    # print(part_two(test_data) == 30)

    # ---- REAL DATA ----
    data = read_data("./2023/data/day06-input.txt")
    print(data)

    # Solution for part A
    print("\n-- Solution for part A:")
    print(part_one(data))  # 1413720
    #
    # # Solution for part B
    # print("\n-- Solution for part B:")
    # print(part_two(data))  # 5667240
