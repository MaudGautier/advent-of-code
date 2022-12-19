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


# def select_best_tunnel(valves, tunnels):
#     closed_valves = [valve for valve in tunnels if valves[valve]["opened"] == False]
#     sorted_valves = sorted(closed_valves, key=lambda x: valves[x]["flow"], reverse=True)
#     # print(sorted_valves)
#     return sorted_valves[0]


# def part_one(valves):
#     current_valve = 'AA'
#     minute = 0
#     while minute < 30:
#         # 1 minute: Select tunnel + go through tunnel
#         minute += 1
#         print("== Minute", minute)
#         tunnels = valves[current_valve]["tunnels"]
#         selected_tunnel = select_best_tunnel(valves, tunnels)
#         print("Move to valve", selected_tunnel)
#         # 1 minute: Open tunnel
#         print("== Minute", minute)
#         minute += 1
#         current_valve = selected_tunnel
#         valves[current_valve]["opened"] = True
#         print("Open valve", selected_tunnel)


# def define_possible_paths(valves):
#     current_valve = 'AA'
#     for i in range(30):
#         next_valves =

# bfs
# def dfs
# def find_next_valve(valves, valve):
#     for i in range(30):
# def compute_all_trees_of_depth(valves, depth):

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
        paths.append((current_path, flow + new_flow))
        # Do not need current_path in principle (at least for part 1) - return it anyway to check
        return flow

    for next_valve in unvisited:
        # To get to valve + open the valve
        additional_turns = shortest_paths[current_valve][next_valve] + 1
        # Stop exploring if end node
        if additional_turns == 1 or current_turn + additional_turns > max_turns:
            additional_flow = (max_turns - current_turn) * rate
            paths.append((current_path, flow + additional_flow))
            continue

        new_rate = valves[next_valve].get("rate", 0)
        # remaining_time = max_turns - current_turn - additional_turns
        additional_flow = rate * additional_turns

        # turn = current_turn + rate *
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


# From solution2:
# XZ': {'TB': 6, 'SY': 7, 'EH': 4, 'ZE': 7, 'RZ': 7, 'FN': 4, 'GH': 3, 'YL': 7, 'IA': 5, 'WK': 5, 'HK': 5, 'WG': 2, 'XU': 5, 'BH': 4, 'OI': 7, 'WE': 6, 'AC': 7, 'EI': 1, 'CP': 3, 'WZ': 7, 'EZ': 7, 'LI': 5, 'WJ': 4, 'AQ': 5, 'DW': 2, 'OA': 3, 'ZV': 7, 'CH': 3, 'CG': 2, 'EX': 4, 'DN': 5, 'QU': 2, 'QA': 7, 'DL': 5, 'BF': 5, 'OJ': 6, 'MN': 5, 'WY': 2, 'PF': 6, 'EK': 1, 'GA': 4, 'BW': 5, 'YZ': 7, 'VG': 5, 'OD': 2, 'GM': 6, 'YP': 3, 'SK': 6, 'PN': 3, 'AA': 4, 'AL': 4, 'OV': 6, 'ZO': 8, 'HJ': 6, 'KB': 5, 'OL': 4, 'PV': 4, 'PU': 6, 'GD': 6, 'GS': 2, 'XZ': 2}}
def part_one(valves):
    shortest_paths = define_shortest_paths(valves)
    # print(shortest_paths)

    # unvisited_valves correspond to closed valves or valves not worth visiting (rate = 0)
    unvisited_valves = {valve_name for valve_name in valves if valves[valve_name].get("rate", 0) != 0}
    # print(unvisited_valves)
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
    # print(paths)
    max_val = 0
    for path in paths:
        max_val = max(max_val, path[1])
        # print(path[1])
    return max_val
    # Puis explorer l'arbre des unvisited (= on ouvre la valve) et calculer pour chaque path son flow total
    # Puis on prend le max des paths
    # possible_paths = define_possible_paths(valves)


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
    # paths = []
    # aa(test_data, 'AA', paths, [], 15)
    # print(paths)
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
