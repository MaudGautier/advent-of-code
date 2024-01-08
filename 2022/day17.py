# x: 0 1 2 3
# y:
# 2
# 1
# 0
import math
from types import SimpleNamespace


class Shape:
    # x and y are bottom left coordinates
    def __init__(self, x, y):
        self.x = x  # horizontal position
        self.y = y  # depth
        self.points = []

    def move_down(self):
        self.y -= 1
        new_points = []
        for point_x, point_y in self.points:
            new_points.append((point_x, point_y - 1))
        self.points = new_points

    def move_left(self):
        self.x -= 1
        new_points = []
        for point_x, point_y in self.points:
            new_points.append((point_x - 1, point_y))
        self.points = new_points

    def move_right(self):
        self.x += 1
        new_points = []
        for point_x, point_y in self.points:
            new_points.append((point_x + 1, point_y))
        self.points = new_points

    def get_points(self):
        return self.points

    def get_bottom_left_coord(self):
        coordinates = {"x": self.x, "y": self.y}
        return SimpleNamespace(**coordinates)


class Rock1(Shape):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.id = 1
        self.shape = "-"
        self.points = [(x, y), (x + 1, y), (x + 2, y), (x + 3, y)]


class Rock2(Shape):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.id = 2
        self.shape = "+"
        self.points = [(x + 1, y), (x, y + 1), (x + 1, y + 1), (x + 2, y + 1), (x + 1, y + 2)]


class Rock3(Shape):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.id = 3
        self.shape = "L"
        self.points = [(x, y), (x + 1, y), (x + 2, y), (x + 2, y + 1), (x + 2, y + 2)]


class Rock4(Shape):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.id = 4
        self.shape = "|"
        self.points = [(x, y), (x, y + 1), (x, y + 2), (x, y + 3)]


class Rock5(Shape):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.id = 5
        self.shape = "ù"
        self.points = [(x, y), (x, y + 1), (x + 1, y), (x + 1, y + 1)]


def select_rock(rock_id, x, y):
    if rock_id == 1:
        rock = Rock1(x, y)
    if rock_id == 2:
        rock = Rock2(x, y)
    if rock_id == 3:
        rock = Rock3(x, y)
    if rock_id == 4:
        rock = Rock4(x, y)
    if rock_id == 5:
        rock = Rock5(x, y)
    return rock


CAVE_WIDTH = 7


def is_move_valid(rock, jet, settled_points):
    rock_points = rock.get_points()
    # if jet is None: # Case rock moving down => need to check all other rocks

    for x, y in rock_points:
        if jet == ">":
            shifted_x = (x + 1)
            if shifted_x >= CAVE_WIDTH or (shifted_x, y) in settled_points:
                return False
        if jet == "<":
            shifted_x = (x - 1)
            if shifted_x < 0 or (shifted_x, y) in settled_points:
                return False

        if jet is None:  # case move down
            shifted_y = (y - 1)
            if (x, shifted_y) in settled_points:
                return False

    return True


def shift_rock(rock, jet, settled_points):
    if jet == ">" and is_move_valid(rock, jet, settled_points):
        rock.move_right()
    if jet == "<" and is_move_valid(rock, jet, settled_points):
        rock.move_left()
    # print("After jet", jet, ":", rock.get_bottom_left_coord(), rock.get_points(), "JET MOVE VALID?",
    #       is_move_valid(rock, jet, settled_points))


def move_rock_down(rock, settled_points):
    if is_move_valid(rock, None, settled_points):
        rock.move_down()
    # print("After down:", rock.get_bottom_left_coord(), rock.get_points())


def has_settled(rock, settled_points):
    if rock.get_bottom_left_coord().y == 0:
        return True
    rock_points = rock.get_points()
    for x, y in rock_points:
        if (x, y - 1) in settled_points:
            return True

    return False


def compute_next_y(current_height):
    # max_y = 0
    # for _, y in current_rock_points:
    #     max_y = max(max_y, y)

    return current_height + 3 + 1 + 1  # 1 for index + 1 higher to start with down


def compute_height(height, rock):
    rock_points = rock.get_points()
    for _, y in rock_points:
        height = max(height, y)

    return height


def settle_rocks(jets, n_rocks, init_phase, period):
    n_turns = min(n_rocks + 1, init_phase + period)
    all_settled_points = set()

    number_rocks_settled = 0
    number_rocks_seen = 0
    next_y = 4  # 1 higher to start with down
    jets_length = len(jets)
    number_jet_applied = 0
    current_height = 0
    heights_sequence = []
    while number_rocks_settled < n_turns:
        # Create new rock
        rock_id = number_rocks_seen % 5 + 1
        rock = select_rock(rock_id, 2, next_y)
        number_rocks_seen += 1
        # print("\n=== NEW ROCK", number_rocks_seen, "(#", rock.id, rock.shape, "):", rock.get_bottom_left_coord(), ":",
        #       rock.get_points(), )

        rock_has_settled = False
        while not rock_has_settled:
            # Move rock down
            move_rock_down(rock, all_settled_points)

            # Move rock with gas jet
            jet_id = number_jet_applied % jets_length
            jet = jets[jet_id]
            shift_rock(rock, jet, all_settled_points)
            number_jet_applied += 1

            if has_settled(rock, all_settled_points):
                rock_has_settled = True
                number_rocks_settled += 1
                all_settled_points.update(rock.get_points())
                # print("Rock at end", rock.get_points())
                previous_height = current_height
                current_height = compute_height(current_height, rock)
                next_y = compute_next_y(current_height)
                heights_sequence.append(current_height - previous_height)

    # print(heights_sequence)

    return (current_height - 1, heights_sequence)


def part_one(jets):
    return settle_rocks(jets, 2022, math.inf, math.inf)[0]


def part_two(jets, period, init_phase):
    # period and init_phase values obtained empirically by printing difference of heights at each round
    # FOR REAL DATA
    # >> > len(init)
    # 229
    # >> > len(period)
    # 1745
    # >> > len(wind)
    # 10091

    finish = 1000000000000
    current_height, diff_heights_sequence = settle_rocks(jets, 2022, init_phase, period)
    periodic_diff_heights = diff_heights_sequence[init_phase:]
    init_diff_heights = diff_heights_sequence[:init_phase]
    print(len(periodic_diff_heights) == period)
    print(len(init_diff_heights) == init_phase)

    to_add_at_each_period = sum(periodic_diff_heights)
    print("to_add_at_each_period", to_add_at_each_period)

    number_cycles = (finish - init_phase) // period
    remaining = (finish - init_phase) % period
    print("number_cycles", number_cycles)

    print(finish == number_cycles * period + init_phase + remaining)
    print(finish, number_cycles * period + init_phase, remaining)

    heights_init_phase = sum(init_diff_heights)
    heights_periods = sum(periodic_diff_heights) * number_cycles
    remaining_heights = sum(periodic_diff_heights[:remaining])

    total_height = heights_init_phase + heights_periods + remaining_heights

    return total_height + 1


def read_data(file_name):
    with open(file_name, 'r') as file:
        return file.readlines()[0]


if __name__ == "__main__":
    # ---- TEST DATA -----
    test_data = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"
    print("-- Tests on test data:")
    print(part_one(test_data) == 3068)
    print(part_two(test_data, 35, 18) == 1514285714288)

    # ---- REAL DATA ----
    data = read_data("./data/2022/day17-input.txt")

    # Solution for part A
    print("\n-- Solution for part A:")
    print(part_one(data))  # 3202

    # Solution for part B
    print("\n-- Solution for part B:")
    print(part_two(data, 1745, 229))  # 1591977077352
