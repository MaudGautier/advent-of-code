ORE, CLAY, OBSIDIAN, GEODE = "ore", "clay", "obsidian", "geode"
MATERIALS = [ORE, CLAY, OBSIDIAN, GEODE]
ROBOTS = [ORE, CLAY, OBSIDIAN, GEODE]


def build_options(blueprint, owned_materials):
    options = {None}
    for robot in [ORE, CLAY, OBSIDIAN, GEODE]:
        costs = blueprint[robot]
        if all(quantity_needed <= owned_materials[material] for material, quantity_needed in costs.items()):
            options.add(robot)
    # OPTIMISATION #2: if Geode can be built => build only this one
    if GEODE in options:
        return {GEODE}

    return options


def harvest(robots, materials):
    new_materials = materials.copy()
    for robot, nb_robot in robots.items():
        new_materials[robot] += nb_robot * 1

    return new_materials


def build_robot(robot, robots, materials, blueprint):
    new_robots = robots.copy()
    new_materials = materials.copy()
    robot_cost = blueprint[robot]
    for k, v in robot_cost.items():
        new_materials[k] -= v
    new_robots[robot] += 1
    return new_robots, new_materials


def get_max_robots(blueprint):
    max_robots = {robot: 0 for robot in blueprint}
    for robot, _ in max_robots.items():
        for r, costs in blueprint.items():
            if costs[robot] >= max_robots[robot]:
                max_robots[robot] = costs[robot]
    max_robots[GEODE] = 100
    return max_robots


def compute_potential(robots, materials, remaining_time):
    # Under the optimistic assumption that 1 geode robot is added every minute
    # Max acquirable = sum of 0 --> n (with n = time_remaining) - at each step: add previous nb of rocks + what collected with new robots
    max_acquirable = remaining_time * (remaining_time - 1) / 2
    return materials[GEODE] + robots[GEODE] * remaining_time + max_acquirable


# Règles d'optim:
# 1) Ne pas build plus que max de robots pour 1 donné OK - ça optimise beaucoup (presque autant, mais moins, que les skipped (#4))
# 2) Si peut construire géode => on construit géode OK - ça optimise un petit peu mais moins que les best au time (#3)
# 3) Que les best au time donné OK - ça optimise un peu mais moins que les skipped (#4)
# 4) Si skipped au dernier coup => on ne le compute pas OK - ça optimise à balle
# 5) Si potentiel < max_potential => on ne continue pas (pas nécessaire pour optim) OK - optimise ~ comme #3 (un peu plus d'optim)

# Ordre des optim les + utiles:
# 4) Si skipped au dernier coup
# 1) Ne pas build plus que max de robots pour 1 donné
# 5) Si potentiel < max_potential => on ne continue pas
# 3) Que les best au time donné
# 2) Si peut construire géode => on construit géode

def dfs(blueprint, end_time):
    materials = {material: 0 for material in MATERIALS}
    robots = {robot: 0 for robot in ROBOTS}
    robots[ORE] = 1

    max_robots = get_max_robots(blueprint)
    # print("MAX ROBOTS", max_robots)

    queue = [(robots, materials, 0, set())]

    nb_iterations = 0
    best_at_time = {time: 0 for time in range(end_time + 1)}
    # print(best_at_time)

    max_nb_geodes_if_this_state_until_end = 0

    while len(queue) > 0:
        nb_iterations += 1
        if nb_iterations % 100000 == 0:
            print("\n---- at iteration", nb_iterations, "(time:", time, "):", len(queue), "Best at time",
                  best_at_time)
        robots, materials, time, skipped_at_last_iteration = queue.pop(0)
        # print("\n---- at iteration", nb_iterations, ":", len(queue) + 1)
        # print("robots", robots)
        # print("materials", materials)

        # OPTIMISATION #5: if potential is smaller than what would happen with no change => do not compute
        remaining_time = end_time - time
        potential = compute_potential(robots, materials, remaining_time)
        if potential < max_nb_geodes_if_this_state_until_end:
            continue
        max_nb_geodes_if_this_state_until_end = max(materials[GEODE] + remaining_time * robots[GEODE],
                                                    max_nb_geodes_if_this_state_until_end)

        # OPTIMISATION #3: Run only for the ones which are already the biggest number of geodes
        best_at_time[time] = max(best_at_time[time], materials[GEODE])
        if time < end_time and materials[GEODE] == best_at_time[time]:
            new_robot_options = build_options(blueprint, materials)
            for robot_to_build in new_robot_options:
                if robot_to_build is None:
                    new_materials = harvest(robots, materials)
                    queue.append((robots.copy(), new_materials, time + 1, new_robot_options - {None}))
                # OPTIMISATION #1: Do not build more than max useful robots of each kind
                elif robots[robot_to_build] + 1 > max_robots[robot_to_build]:
                    continue
                # OPTIMISATION #4: Do not build a robot that was skipped at last iteration
                elif robot_to_build in skipped_at_last_iteration:
                    continue
                else:
                    new_robots, new_materials = build_robot(robot_to_build, robots, materials, blueprint)
                    new_materials = harvest(robots, new_materials)
                    queue.append((new_robots.copy(), new_materials.copy(), time + 1, set()))

    # print("Total number of iterations", nb_iterations, best_at_time)
    return best_at_time[end_time]


def convert_data_to_blueprints(lines):
    blueprints = []
    for line in lines:
        materials = {material: 0 for material in MATERIALS}
        blueprint = {robot: materials.copy() for robot in ROBOTS}

        key, robots_costs = line.strip().split(":")
        for robot_costs in robots_costs.split(".")[:-1]:
            robot_name = robot_costs.split(" ")[2]
            costs = robot_costs.split(" costs ")[1]
            individual_costs = costs.split(" and ")
            for individual_cost in individual_costs:
                qty, mat_name = individual_cost.split(" ")
                blueprint[robot_name][mat_name] = int(qty)
        blueprints.append(blueprint)
    return blueprints


def part_one(blueprints, end_time):
    id = 0
    summed_value = 0
    for blueprint in blueprints:
        id += 1
        value = dfs(blueprint, end_time)
        summed_value += value * (id)
    return summed_value


def read_data(file_name):
    with open(file_name, 'r') as file:
        return file.readlines()


if __name__ == "__main__":
    # ---- TEST DATA -----
    sub_test_data_1 = "Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian."
    print("-- Tests on test data:")
    # test_blueprint1 = {
    #     "ore": {"ore": 4, "clay": 0, "obsidian": 0, "geode": 0},
    #     "clay": {"ore": 2, "clay": 0, "obsidian": 0, "geode": 0},
    #     "obsidian": {"ore": 3, "clay": 14, "obsidian": 0, "geode": 0},
    #     "geode": {"ore": 2, "clay": 0, "obsidian": 7, "geode": 0},
    # }
    test_blueprint1 = convert_data_to_blueprints([sub_test_data_1])[0]
    print(dfs(test_blueprint1, 24) == 9)

    sub_test_data_2 = "Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian."
    # test_blueprint2 = {
    #     "ore": {"ore": 2, "clay": 0, "obsidian": 0, "geode": 0},
    #     "clay": {"ore": 3, "clay": 0, "obsidian": 0, "geode": 0},
    #     "obsidian": {"ore": 3, "clay": 8, "obsidian": 0, "geode": 0},
    #     "geode": {"ore": 3, "clay": 0, "obsidian": 12, "geode": 0},
    # }
    test_blueprint2 = convert_data_to_blueprints([sub_test_data_2])[0]
    print(dfs(test_blueprint2, 24) == 12)
    test_blueprints = convert_data_to_blueprints([sub_test_data_1, sub_test_data_2])
    print(part_one(test_blueprints, 24) == 33)

    # ---- REAL DATA ----
    data = read_data("./2022/data/day19-input.txt")

    # Solution for part A
    print("\n-- Solution for part A:")
    blueprints = convert_data_to_blueprints(data)
    print(part_one(blueprints, 24))  # 1675

    # # Solution for part B
    # print("\n-- Solution for part B:")
    # print(part_two(data))  # 3316 INCORRECT TOO HIGH # 2072 TOO LOW # Correct = 2090 surface (1060 trapped)
