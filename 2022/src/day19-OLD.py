# def read_data(file_name):
#     with open(file_name, 'r') as file:
#         return file.readlines()[0]

# Structure
# Possessions:
# rocks = {"ore": 1, "clay": 2, "obsidian": 2, "geode": 0}
# robots = {"ore": 1, "clay": 0, "obsidian": 0, "geode": 0}
# Items:
# robots_costs = { "ore": {"ore": 4}, "clay": {"ore": 2}}

# def one_round(possessed_rocks, possessed_robots, robots_costs):
#     # Chaque tour:
#     # Chaque robot collecte ses pierres ( => ajoute aux possessions)
#     # Ajout robots: Regarde liste des sets de robots achetables => pour chaque = node, ajoute à la liste des robots et supprime les pierres utilisées et relance un tour
#     # Stop condition = si minute >=24
#
#     # Stop condition
#     # if minute >= 24:
#     #     paths.append()


OPTIMISED_ROBOT = "clay"  # "geode"


def can_buy_robot(robot_costs, available_rocks):
    for rock, cost in robot_costs.items():
        if available_rocks[rock] < cost:
            return False
    return True


def compute_potential(owned_robots, owned_rocks, time_remaining):
    # new_rocks = owned_rocks.copy()
    # new_robots = owned_robots.copy()
    # new_robots[new_robot] += 1
    # new_rocks
    # nb_acquirable_geode_robots = time_remaining
    # 3 remaining: 3) +1 robot, 2) +1 rock + 2 robots 1) 1+2 rocks + 3 robots ###### 0) 1+2+3 + 4 robots
    # = 1*(time-1) + 2 * (time-2) + 3 *(time-3) + ....

    # 0 remaining: 0
    # 1 remaining: 1) + 1 robot
    # 2 remaining: 2) + 1 robot, 1) + 1+1 robot + 1 rock == 1 rock
    # 3 remaining: 3) + 1 robot, 2) + 1+1 robot + 1 rock 1) + 1+1 robot + 1+2 rock == 3 rock
    #

    # Under the optimistic assumption that 1 geode robot is added every minute
    # Max acquirable = sum of 0 --> n (with n = time_remaining) - at each step: add previous nb of rocks + what collected with new robots
    max_acquirable = time_remaining * (time_remaining - 1) / 2
    return owned_rocks[OPTIMISED_ROBOT] + time_remaining * owned_robots[OPTIMISED_ROBOT] + max_acquirable


# queue = queue des états à parcourir (robots, materials, time)
# while queue: for robot in blueprint => soit on peut ajouter le robot (= matos plus élevé que besoin pour chaque) => ajoute robot et append, soit on peut pas ajouter => on n'ajoute pas et append


def is_not_useful_anymore(rock, owned_robots, owned_rocks, time_remaining, blueprint):
    if rock == OPTIMISED_ROBOT:
        return False
    max_amount_required = max([robot_costs[rock] for rob, robot_costs in blueprint.items()])
    if owned_rocks[rock] + time_remaining * owned_robots[rock] >= time_remaining * max_amount_required:
        return True
    return False


def compute_useful_robots(owned_robots, owned_rocks, time_remaining, blueprint):
    # For any resource R that's not geode:
    # if you already have X robots creating resource R,
    # a current stock of Y for that resource,
    # T minutes left,
    # and no robot requires more than Z of resource R to build,
    # and X * T+Y >= T * Z,
    # then you never need to build another robot mining R anymore.
    useful_robots = ["geode"]
    for rock in ["ore", "clay", "obsidian"]:
        max_amount_required = max([robot_costs[rock] for rob, robot_costs in blueprint.items()])
        # print(rock, max_amount_required)
        # print("for rock", rock, ":", owned_rocks[rock] + time_remaining * owned_robots[rock],
        #       time_remaining * max_amount_required)
        if owned_rocks[rock] + time_remaining * owned_robots[rock] < time_remaining * max_amount_required:
            useful_robots.append(rock)

    return useful_robots

    # for robot, robot_costs in blueprint.items():


def compute_possible_robots(owned_rocks, blueprint):
    possible_robots = {"ore"}
    for robot, robot_costs in blueprint.items():
        if can_buy_robot(robot_costs, owned_rocks):
            possible_robots.add(robot)
    if OPTIMISED_ROBOT in possible_robots:
        return {OPTIMISED_ROBOT}
    return possible_robots


def dfs():
    init_robots = {"ore": 1, "clay": 0, "obsidian": 0, "geode": 0}
    init_rocks = {"ore": 0, "clay": 0, "obsidian": 0, "geode": 0}
    init_time_remaining = 24
    blueprint = {
        "ore": {"ore": 4, "clay": 0, "obsidian": 0, "geode": 0},
        "clay": {"ore": 2, "clay": 0, "obsidian": 0, "geode": 0},
        "obsidian": {"ore": 3, "clay": 14, "obsidian": 0, "geode": 0},
        "geode": {"ore": 2, "clay": 0, "obsidian": 7, "geode": 0},
    }
    queue = [(init_robots, init_rocks, init_time_remaining)]
    # max_ore_robots = 4 + 2 + 3 + 2
    # max_clay_robots = 14
    # max_obsidian_robots = 7
    max_robots = {
        "ore": 4, "clay": 14, "obsidian": 7, "geode": 100
    }
    max_robots[OPTIMISED_ROBOT] = 100

    # owned_rocks = init_rocks
    # owned_robots = init_robots
    # time_remaining = init_time_remaining

    number_it = 0
    max_number_geodes_if_this_state_until_end = 0
    while len(queue) > 0:
        number_it += 1
        if number_it % 100000 == 0:
            print("\n----", number_it, ":", len(queue), "(time:", time_remaining, ") best so far:",
                  max_number_geodes_if_this_state_until_end)
        # print("\n----- queue", len(queue), queue)
        # if len(queue) > 1 and queue[0] == queue[1]:
        #     print("FIRST TWO IDENTICAL")
        owned_robots, owned_rocks, time_remaining = queue.pop(0)
        # print("robots", owned_robots)
        # print("rocks", owned_rocks)
        # print("time", time_remaining)
        max_number_geodes_if_this_state_until_end = max(
            owned_rocks[OPTIMISED_ROBOT] + owned_robots[OPTIMISED_ROBOT] * time_remaining,
            max_number_geodes_if_this_state_until_end)
        # print("max_number_clays_if_this_state_until_end", owned_rocks["clay"] + owned_robots["clay"] * time_remaining)

        potential = compute_potential(owned_robots, owned_rocks, time_remaining)
        if potential <= max_number_geodes_if_this_state_until_end:
            continue

        if time_remaining - 1 >= 0:
            can_buy = False

            # NE FONCTIONNE PAS
            # useful_robots = compute_useful_robots(owned_robots, owned_rocks, time_remaining, blueprint)
            # print(useful_robots)

            possible_robots = compute_possible_robots(owned_rocks, blueprint)
            for robot in possible_robots:
                robot_costs = blueprint[robot]

                # for robot, robot_costs in blueprint.items():
                # for robot in useful_robots:
                #     robot_costs = blueprint[robot]
                # print("ROBOT", robot, can_buy_robot(robot_costs, owned_rocks))
                # You can buy an additional robot
                if is_not_useful_anymore(robot, owned_robots, owned_rocks, time_remaining, blueprint):
                    continue
                # Cut if more robots than needed
                if owned_robots[robot] + 1 > max_robots[robot]:
                    continue
                # if robot == "ore" and owned_robots[robot] + 1 >= max_ore_robots:
                #     # print("PRUNE ore")
                #     continue
                # if robot == "clay" and owned_robots[robot] + 1 >= max_clay_robots:
                #     # print("PRUNE clay")
                #     continue
                # if robot == "obsidian" and owned_robots[robot] + 1 >= max_obsidian_robots:
                #     # print("PRUNE obsidian")
                #     continue
                if can_buy_robot(robot_costs, owned_rocks):
                    # You choose to buy it
                    can_buy = True
                    new_robots = owned_robots.copy()
                    new_robots[robot] += 1
                    new_rocks = owned_rocks.copy()
                    for rock, cost in robot_costs.items():
                        new_rocks[rock] -= cost
                    for robot, nb_robot in owned_robots.items():
                        new_rocks[robot] += nb_robot * 1
                    queue.append((new_robots, new_rocks, time_remaining - 1))
                    # You choose *NOT* to buy it (probably do not want this - assumption: if can buy => buy it)
                    new_rocks = owned_rocks.copy()
                    for robot, nb_robot in owned_robots.items():
                        new_rocks[robot] += nb_robot * 1
                    queue.append((owned_robots, new_rocks, time_remaining - 1))

            # You *Cannot* buy an additional robot
            if can_buy is False:
                new_rocks = owned_rocks.copy()
                for robot, nb_robot in owned_robots.items():
                    new_rocks[robot] += nb_robot * 1
                queue.append((owned_robots, new_rocks, time_remaining - 1))

    print("for init_time_remaining", init_time_remaining, "rock optimised", OPTIMISED_ROBOT, "-- TOTAL NB IT:",
          number_it)

    return max_number_geodes_if_this_state_until_end


if __name__ == "__main__":
    # ---- TEST DATA -----
    sub_test_data_1 = "Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian."
    sub_test_data_2 = "Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian."
    print("-- Tests on test data:")
    print(dfs())
    # print(compute_max_opened_geodes(sub_test_data_1, 24) == 9)
    # print(part_two(test_data) == 1514285714288)

    # # ---- REAL DATA ----
    # data = read_data("./2022/data/day19-input.txt")
    #
    # # Solution for part A
    # print("\n-- Solution for part A:")
    # print(part_one(data))  # 3202
    #
    # # Solution for part B
    # print("\n-- Solution for part B:")
    # print(part_two(data))  # 1591977077352
