import math


def read_data(file_name):
    with open(file_name, 'r') as file:
        return file.read()[:-1]


def read_parts(data: str):
    parts = data.split("\n\n")
    d = {}
    d["seeds"] = [int(seed) for seed in parts[0].split(": ")[1].split(" ")]
    for part in parts[1:]:
        name = part.split(" map:\n")[0]
        subsets = part.split(" map:\n")[1].split("\n")

        SDL = []
        for subset in subsets:
            destination, source, length = subset.split(" ")
            SDL.append((int(source), int(destination), int(length)))
        SDL.sort()

        d[name] = SDL

    return d


def convert(parts, part_name, origin):
    for source, dest, length in parts[part_name]:
        if source <= origin < source + length:
            return origin - source + dest
    return origin


def part_one(data: str) -> int:
    parts = read_parts(data)
    min_location = math.inf
    for seed in parts["seeds"]:
        soil = convert(parts, "seed-to-soil", seed)
        fertilizer = convert(parts, "soil-to-fertilizer", soil)
        water = convert(parts, "fertilizer-to-water", fertilizer)
        light = convert(parts, "water-to-light", water)
        temperature = convert(parts, "light-to-temperature", light)
        humidity = convert(parts, "temperature-to-humidity", temperature)
        location = convert(parts, "humidity-to-location", humidity)
        min_location = min(min_location, location)

    return min_location


if __name__ == "__main__":
    # ---- TEST DATA -----
    test_data = '''seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4'''
    print("-- Tests on test data:")
    print(part_one(test_data) == 35)
    # print(part_two(test_data) == 30)

    # ---- REAL DATA ----
    data = read_data("./2023/data/day05-input.txt")

    # Solution for part A
    print("\n-- Solution for part A:")
    print(part_one(data))  # 662197086
    #
    # # Solution for part B
    # print("\n-- Solution for part B:")
    # print(part_two(data))  # 5667240
