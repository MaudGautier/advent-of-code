def extract_coordinates(element):
    coordinates = element.split(" at ")[1].split(", ")
    x = int(coordinates[0].split("=")[1])
    y = int(coordinates[1].split("=")[1])
    return (x, y)


# Structure:
# data = [
#   ((x_sensor_1, y_sensor_1), (x_beacon_1, y_beacon_1)),
#   ((x_sensor_2, y_sensor_2), (x_beacon_2, y_beacon_2)),
# ]
def convert_lines_to_data(lines):
    data = []
    for line in lines:
        sensor, beacon = line.split(":")
        sensor_coordinates = extract_coordinates(sensor)  # .split(" at ")[1]
        beacon_coordinates = extract_coordinates(beacon)  # beacon.split(" at ")[1]
        data.append((sensor_coordinates, beacon_coordinates))
    return data


def read_data(file_name):
    with open(file_name, 'r') as file:
        lines = [line for line in file.readlines()]
        return convert_lines_to_data(lines)


def compute_manhattan_distance(sensor, beacon):
    x_sensor, y_sensor = sensor
    x_beacon, y_beacon = beacon
    manhattan_distance = abs(x_sensor - x_beacon) + abs(y_sensor - y_beacon)

    return manhattan_distance


# WARNING: in schema, x and y reversed
def compute_y_distance(sensor, y_row):
    _, y_sensor = sensor
    return abs(y_sensor - y_row)


def compute_sensor_trace_start_end_in_line(sensor, beacon, y_row):
    x_sensor, _ = sensor
    manhattan_distance = compute_manhattan_distance(sensor, beacon)
    y_distance_to_line = compute_y_distance(sensor, y_row)
    # If manhattan distance is smaller than y_distance to line => NO overlap
    if manhattan_distance < y_distance_to_line:
        return None

    start = x_sensor - abs(manhattan_distance - y_distance_to_line)
    end = x_sensor + abs(manhattan_distance - y_distance_to_line)
    return start, end


# structure: limits = [(start, end), (start, end), (start, end)...] (for all sensors)
def compute_trace_limits_in_row(records, y_row):
    limits = []
    for sensor, beacon in records:
        trace = compute_sensor_trace_start_end_in_line(sensor, beacon, y_row)
        if trace is not None:
            limits.append(trace)
    return limits


def get_union(intervals):
    sorted_intervals = sorted(intervals)
    merged_intervals = []
    for begin, end in sorted_intervals:
        if merged_intervals and merged_intervals[-1][1] >= begin - 1:
            merged_intervals[-1][1] = max(merged_intervals[-1][1], end)
        else:
            merged_intervals.append([begin, end])

    return merged_intervals


def find_points_filled_in_line(records, y_row):
    points_on_line = []
    for sensor, beacon in records:
        x_sensor, y_sensor = sensor
        x_beacon, y_beacon = beacon

        if y_sensor == y_row:
            points_on_line.append(x_sensor)
        if y_beacon == y_row:
            points_on_line.append(x_beacon)

    return set(points_on_line)


def count_empty_points_in_line(trace_union, records, y_row):
    points_filled_in_line = find_points_filled_in_line(records, y_row)

    number_points_in_trace = 0
    for point in points_filled_in_line:
        for start, end in trace_union:
            if start <= point <= end:
                number_points_in_trace += 1

    len_trace = sum([end - start + 1 for start, end in trace_union])

    return len_trace - number_points_in_trace


## Option 1 (non efficace car grille principalement vide ??)
# 1. ?? Draw map of sensors and beacon
# 2. Pour tous les sensors, fill grid with #
# 3. Récupère ligne 10 de grid
#
## Option 2??? (sûrement meilleur car pas d'espaces vides)
# 1. Pour tous les sensors, définit tous les espaces où B ne peut pas être (array des positions d'absence)
# 2. Récupère ceux qui ont x = 10
def part_one(records, y_row):
    trace_limits_in_row = compute_trace_limits_in_row(records, y_row)
    trace_union = get_union(trace_limits_in_row)
    # print(trace_union)
    return count_empty_points_in_line(trace_union, records, y_row)


if __name__ == "__main__":
    # ---- TEST DATA -----
    test_lines = [
        "Sensor at x=2, y=18: closest beacon is at x=-2, y=15",
        "Sensor at x=9, y=16: closest beacon is at x=10, y=16",
        "Sensor at x=13, y=2: closest beacon is at x=15, y=3",
        "Sensor at x=12, y=14: closest beacon is at x=10, y=16",
        "Sensor at x=10, y=20: closest beacon is at x=10, y=16",
        "Sensor at x=14, y=17: closest beacon is at x=10, y=16",
        "Sensor at x=8, y=7: closest beacon is at x=2, y=10",
        "Sensor at x=2, y=0: closest beacon is at x=2, y=10",
        "Sensor at x=0, y=11: closest beacon is at x=2, y=10",
        "Sensor at x=20, y=14: closest beacon is at x=25, y=17",
        "Sensor at x=17, y=20: closest beacon is at x=21, y=22",
        "Sensor at x=16, y=7: closest beacon is at x=15, y=3",
        "Sensor at x=14, y=3: closest beacon is at x=15, y=3",
        "Sensor at x=20, y=1: closest beacon is at x=15, y=3",
    ]
    test_data = convert_lines_to_data(test_lines)
    # test_data = [
    #     ((2, 18), (-2, 15)),
    #     ((9, 16), (10, 16)),
    #     ((13, 2), (15, 3)),
    #     ((12, 14), (10, 16)),
    #     ((10, 20), (10, 16)),
    #     ((14, 17), (10, 16)),
    #     ((8, 7), (2, 10)),
    #     ((2, 0), (2, 10)),
    #     ((0, 11), (2, 10)),
    #     ((20, 14), (25, 17)),
    #     ((17, 20), (21, 22)),
    #     ((16, 7), (15, 3)),
    #     ((14, 3), (15, 3)),
    #     ((20, 1), (15, 3))
    # ]
    print("-- Tests on test data:")
    # print(compute_sensor_trace_start_end_in_line(test_data[0][0], test_data[0][1], 10) == None)
    # print(compute_sensor_trace_start_end_in_line(test_data[1][0], test_data[1][1], 10) == None)
    # print(compute_sensor_trace_start_end_in_line(test_data[2][0], test_data[2][1], 10) == None)
    # print(compute_sensor_trace_start_end_in_line(test_data[3][0], test_data[3][1], 10) == (12, 12))
    print(part_one(test_data, 10) == 26)
    # print(part_two(test_data) == 93)

    # ---- REAL DATA ----
    data = read_data("./2022/data/day15-input.txt")

    # Solution for part A
    print("\n-- Solution for part A:")
    print(part_one(data, 2000000))  # 4861076
    #
    # # Solution for part B
    # print("\n-- Solution for part B:")
    # print(part_two(data))  # 26139
