import math


# structure: {'AA': {'rate': 0, 'tunnels': ['DD', 'II', 'BB']}
def convert_lines_to_data(lines):
    data = {}
    for line in lines:
        part1, part2 = line.split(";")
        flow_rate = int(part1.split("=")[1])
        name = part1[6:8]
        if "valves " in part2:
            tunnels = part2.split("valves ")[1].split(", ")
        elif "valve " in part2:
            tunnels = [part2.split("valve ")[1]]
        data[name] = {"rate": flow_rate, "tunnels": tunnels}

    return data


def read_data(file_name):
    with open(file_name, 'r') as file:
        # print(file)
        lines = [line.strip() for line in file.readlines()]
        print(lines)
        return convert_lines_to_data(lines)


# def compute_all_paths(valves, current_valve, paths, current_path, depth):
#     if depth == 0:
#         current_path.append(current_valve)
#         paths.append(current_path)
#         return
#
#     next_possible_valves = valves[current_valve]["tunnels"]
#     for next_valve in next_possible_valves:
#         compute_all_paths(valves, next_valve, paths, current_path + [current_valve], depth - 1)

def define_shortest_paths(valves):
    shortest_paths = {}
    for valve in valves:
        shortest_paths[valve] = {}
        for next_valve in valves:
            if next_valve in valves[valve].get("tunnels"):
                shortest_paths[valve][next_valve] = 1
            else:
                shortest_paths[valve][next_valve] = math.inf
        shortest_paths[valve][valve] = 0

    for intermediate_valve in valves:
        for valve in valves:
            for next_valve in valves:
                shortest_paths[valve][next_valve] = min(shortest_paths[valve][next_valve],
                                                        shortest_paths[valve][intermediate_valve] +
                                                        shortest_paths[intermediate_valve][next_valve])

    # Check that all are reported
    # print("CHECKING NO MISSING")
    for valve in valves:
        for next_valve in valves:
            # print("-- For couple:", valve, next_valve)
            if shortest_paths[valve][next_valve] == math.inf:
                # print("MISSING")
                raise ("MISSING")

    return shortest_paths


def explore(valves, paths, current_path, flow, unvisited, shortest_paths, current_valve, max_turns, current_turn, rate):
    if len(unvisited) == 0:  # or turn >= max_turns
        new_flow = (max_turns - current_turn) * rate
        # Do not need current_path in principle (at least for part 1) - return it anyway to check
        paths.append((current_path, flow + new_flow))
        return flow

    for next_valve in unvisited:
        # To get to valve + open the valve
        additional_turns = shortest_paths[current_valve][next_valve] + 1

        # Stop exploring if end node
        if additional_turns == 1 or current_turn + additional_turns > max_turns:
            additional_flow = (max_turns - current_turn) * rate
            paths.append((current_path, flow + additional_flow))
            continue

        # Explore next valve
        new_rate = valves[next_valve].get("rate", 0)
        additional_flow = rate * additional_turns
        explore(valves=valves,
                paths=paths,
                current_path=current_path + [next_valve],
                flow=flow + additional_flow,
                unvisited=unvisited - {next_valve},
                shortest_paths=shortest_paths,
                current_valve=next_valve,
                max_turns=max_turns,
                current_turn=current_turn + additional_turns,
                rate=rate + new_rate)


def select_best_path(paths):
    max_val = 0
    for path in paths:
        max_val = max(max_val, path[1])
    return max_val


def part_one(valves):
    shortest_paths = define_shortest_paths(valves)

    # unvisited_valves correspond to closed valves or valves not worth visiting (rate = 0)
    unvisited_valves = {valve_name for valve_name in valves if valves[valve_name].get("rate", 0) != 0}

    paths = []
    explore(valves=valves,
            paths=paths,
            current_path=[],
            flow=0,
            unvisited=unvisited_valves,
            shortest_paths=shortest_paths,
            current_valve='AA',
            max_turns=30,
            current_turn=0,
            rate=0)

    return select_best_path(paths)
    # Puis explorer l'arbre des unvisited (= on ouvre la valve) et calculer pour chaque path son flow total
    # Puis on prend le max des paths


if __name__ == "__main__":
    # ---- TEST DATA -----
    test_lines = [
        "Valve AA has flow rate=0; tunnels lead to valves DD, II, BB",
        "Valve BB has flow rate=13; tunnels lead to valves CC, AA",
        "Valve CC has flow rate=2; tunnels lead to valves DD, BB",
        "Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE",
        "Valve EE has flow rate=3; tunnels lead to valves FF, DD",
        "Valve FF has flow rate=0; tunnels lead to valves EE, GG",
        "Valve GG has flow rate=0; tunnels lead to valves FF, HH",
        "Valve HH has flow rate=22; tunnel leads to valve GG",
        "Valve II has flow rate=0; tunnels lead to valves AA, JJ",
        "Valve JJ has flow rate=21; tunnel leads to valve II"
    ]
    test_data = convert_lines_to_data(test_lines)
    # test_data = {
    #   'AA': {'rate': 0, 'tunnels': ['DD', 'II', 'BB']},
    #   'BB': {'rate': 13, 'tunnels': ['CC', 'AA']},
    #   'CC': {'rate': 2, 'tunnels': ['DD', 'BB']},
    #   'DD': {'rate': 20, 'tunnels': ['CC', 'AA', 'EE']},
    #   'EE': {'rate': 3, 'tunnels': ['FF', 'DD']},
    #   'FF': {'rate': 0, 'tunnels': ['EE', 'GG']},
    #   'GG': {'rate': 0, 'tunnels': ['FF', 'HH']},
    #   'HH': {'rate': 22, 'tunnels': ['GG']},
    #   'II': {'rate': 0, 'tunnels': ['AA', 'JJ']},
    #   'JJ': {'rate': 21, 'tunnels': ['II']}
    # }
    print("-- Tests on test data:")
    print(part_one(test_data) == 1651)
    # print(part_two(test_data, 20) == 56000011)

    # ---- REAL DATA ----
    data = read_data("./2022/data/day16-input.txt")

    # Solution for part A
    print("\n-- Solution for part A:")
    print(part_one(data))  # 2080
    #
    # # Solution for part B
    # print("\n-- Solution for part B:")
    # print(part_two(data))  # 10649103160102
