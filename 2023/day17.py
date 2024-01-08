import heapq
import math


def read_data(file_name):
    with open(file_name, 'r') as file:
        return [line.strip() for line in file.readlines()]


Grid = list[list[int]]
Position = tuple[int, int]
Distance = int
Direction = tuple[int, int]
NbMoves = int
Node = tuple[Distance, Direction, NbMoves, Position]


def parse_grid(data: list[str]) -> Grid:
    grid = []
    for line in data:
        grid.append([int(char) for char in line])
    return grid


def get_neighbors(node: Node, grid: Grid, min_moves: int, max_moves: int) -> list[Node]:
    distance, direction, moves_so_far, position = node

    neighbors = []
    for dir in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        # Invalid - too many in direction
        if dir == direction and moves_so_far >= max_moves:
            continue
        if dir != direction and moves_so_far < min_moves:
            continue

        # Define neighbor moves so far
        if dir == direction:
            neighbor_moves_so_far = moves_so_far + 1
        else:
            neighbor_moves_so_far = 1

        neighbor_position = (position[0] + dir[0], position[1] + dir[1])

        # Invalid - not in grid
        if not (0 <= neighbor_position[0] < len(grid) and 0 <= neighbor_position[1] < len(grid[0])):
            continue

        # Invalid - goes back to previous direction
        if dir[0] == -direction[0] and dir[1] == -direction[1]:
            continue

        neighbor_distance = distance + grid[neighbor_position[0]][neighbor_position[1]]
        neighbors.append((neighbor_distance, dir, neighbor_moves_so_far, neighbor_position))

    return neighbors


def run_dijkstra(grid: Grid, start: Position, min_moves: int = 1, max_moves: int = 3) -> int:
    # Initialize
    shortest_path = {}
    max_value = math.inf
    for i, row in enumerate(grid):
        for j in range(len(row)):
            shortest_path[(i, j)] = max_value
    shortest_path[start] = 0

    # Compute score for each node
    visited = set()
    value = 0
    queue = [(value, (0, 1), 0, start),
             (value, (1, 0), 0, start)]  # (distance, direction, moves so far in direction, position)
    while len(queue) > 0:
        # Get node with minimum distance
        node = heapq.heappop(queue)
        node_distance, node_direction, node_moves, node_position = node
        if (node_direction, node_moves, node_position) in visited:
            continue

        # Visit all neighbors
        neighbors = get_neighbors(node, grid, min_moves=min_moves, max_moves=max_moves)
        for neighbor in neighbors:
            distance, direction, moves_so_far, position = neighbor

            # Update distance if shorter
            # But only if moves so far correspond to the requirements
            if min_moves <= moves_so_far <= max_moves:
                if shortest_path[position] > distance:
                    shortest_path[position] = distance

            # Append neighbor to queue
            heapq.heappush(queue, neighbor)

        # Mark node as visited when all neighbors dealt with
        visited.add((node_direction, node_moves, node_position))

    end = (len(grid) - 1, len(grid[0]) - 1)
    return shortest_path[end]


def part_one(data: list[str]) -> int:
    grid = parse_grid(data)
    start = (0, 0)
    return run_dijkstra(grid, start)


def part_two(data: list[str]) -> int:
    grid = parse_grid(data)
    start = (0, 0)
    return run_dijkstra(grid, start, min_moves=4, max_moves=10)


if __name__ == "__main__":
    # ---- TEST DATA -----
    test_data_1 = [
        "35",
        "33"
    ]
    test_data_2 = [
        "563",
        "735",
        "533"
    ]
    test_data_3 = [
        "1419",
        "1919",
        "9219",
        "9311",
    ]
    test_data_4 = [
        "1111",
        "9991",
        "1111",
        "1669",
        "1111",
    ]
    test_data_5 = [
        "36",
        "54",
        "66",
        "53",  # TURN HERE RIGHT
        "87",
        "53",
        "63",  # TURN HERE RIGHT
        "35",
        "33"
    ]
    test_data_6 = [
        "199",
        "199",
        "199",
        # 3 rows above to make sure we have to turn on the next row
        "536",  # TURN DOWN BELOW 3
        "454",
        "766",
        "653",  # TURN HERE RIGHT
        "887",
        "453",
        "563",  # TURN HERE RIGHT
        "735",
        "533"
    ]
    test_data_7 = [
        "1199",
        "9199",
        "9199",
        # 3 rows above to make sure we have to turn on the next row
        "7536",
        "8454",
        "7766",
        "9653",
        "6887",
        "6453",
        "5563",
        "7735",
        "5533"
    ]
    print("-- Tests on subsets of test data:")
    print(part_one(test_data_1) == 6)
    print(part_one(test_data_2) == 15)
    print(part_one(test_data_3) == 4 + 1 + 1 + 1 + 1 + 1)
    print(part_one(test_data_4) == 1 * 3 + 1 + 1 * 4 + 1 + 1 * 4)
    print(part_one(test_data_5) == 5 + 6 + 5 + 3 + 7 + 3 + 3 + 6 + 3 + 3 + 3)
    print(part_one(test_data_6) == 1 * 2 + 5 + 3 + 5 + 6 + 5 + 3 + 7 + 3 + 3 + 6 + 3 + 3 + 3)
    print(part_one(test_data_7) == 1 * 3 + 5 + 3 + 5 + 6 + 5 + 3 + 7 + 3 + 3 + 6 + 3 + 3 + 3)

    test_data = [
        "2413432311323",
        "3215453535623",
        "3255245654254",
        "3446585845452",
        "4546657867536",
        "1438598798454",
        "4457876987766",
        "3637877979653",
        "4654967986887",
        "4564679986453",
        "1224686865563",
        "2546548887735",
        "4322674655533"
    ]
    test_data_other = [
        "111111111111",
        "999999999991",
        "999999999991",
        "999999999991",
        "999999999991"
    ]
    print("\n-- Tests on real test data:")
    print(part_one(test_data) == 102)
    print(part_two(test_data) == 94)
    print(part_two(test_data_other) == 71)

    # ---- REAL DATA ----
    data = read_data("./2023/data/day17-input.txt")

    # Solution for part A
    print("\n-- Solution for part A:")
    print(part_one(data))  # 694

    # Solution for part B
    print("\n-- Solution for part B:")
    print(part_two(data))  # 829

    # NB: takes ~ 4 seconds to execute everything - likely there are some optimisations possible
