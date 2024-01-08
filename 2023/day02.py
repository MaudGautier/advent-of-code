def read_data(file_name):
    with open(file_name, 'r') as file:
        return [line.strip() for line in file.readlines()]


def parse_subset(subset: str):
    balls = subset.split(", ")
    blue, red, green = 0, 0, 0
    for ball in balls:
        if ball.endswith("blue"):
            blue = int(ball.split(" ")[0])
            continue
        if ball.endswith("red"):
            red = int(ball.split(" ")[0])
            continue
        if ball.endswith("green"):
            green = int(ball.split(" ")[0])

    return blue, red, green


def parse_game(game: str):
    game_index = game.split(": ")[0].split(" ")[1]
    subsets = game.split(": ")[1].split("; ")
    max_blue, max_red, max_green = 0, 0, 0
    for subset in subsets:
        blue, red, green = parse_subset(subset)
        max_blue = max(max_blue, blue)
        max_red = max(max_red, red)
        max_green = max(max_green, green)

    return int(game_index), {"blue": max_blue, "red": max_red, "green": max_green}


def part_one(data: list[str], nb_red, nb_green, nb_blue):
    total = 0
    for game in data:
        game_index, max_balls = parse_game(game)
        if max_balls["red"] > nb_red or max_balls["green"] > nb_green or max_balls["blue"] > nb_blue:
            continue
        total += game_index

    return total


def part_two(data: list[str]):
    total = 0
    for game in data:
        _, max_balls = parse_game(game)
        mult = 1
        for ball_count in max_balls.values():
            mult *= ball_count
        total += mult
    return total


if __name__ == "__main__":
    # ---- TEST DATA -----
    test_data = [
        "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green",
        "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue",
        "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red",
        "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red",
        "Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green",
    ]
    print("-- Tests on test data:")
    print(part_one(data=test_data, nb_red=12, nb_green=13, nb_blue=14) == 8)
    print(part_two(data=test_data) == 2286)

    # ---- REAL DATA ----
    data = read_data("./2023/data/day02-input.txt")

    # Solution for part A
    print("\n-- Solution for part A:")
    print(part_one(data=data, nb_red=12, nb_green=13, nb_blue=14))  # 2085

    # Solution for part B
    print("\n-- Solution for part B:")
    print(part_two(data=data))  # 79315
