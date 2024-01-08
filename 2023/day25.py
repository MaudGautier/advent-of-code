import random
from collections import deque


def read_data(file_name):
    with open(file_name, 'r') as file:
        return file.read().strip()


Node = str
Graph = dict[Node, list[Node]]


def parse_data(data: str) -> Graph:
    graph = {}
    for line in data.splitlines():
        node, linked_nodes = line.split(": ")
        for linked_node in linked_nodes.split(" "):
            graph[node] = graph.get(node, []) + [linked_node]
            graph[linked_node] = graph.get(linked_node, []) + [node]
    return graph


def get_shortest_path(graph: Graph, start: Node, end: Node):
    # This is a BFS
    to_visit = deque()
    to_visit.append((start, []))
    while len(to_visit) > 0:
        node, path = to_visit.popleft()
        if node == end:
            return path
        for neighbor in graph[node]:
            if neighbor in path:
                continue
            to_visit.append((neighbor, path + [node]))


def create_group(graph: Graph, start: Node) -> list[Node]:
    group = []

    nodes_to_append_to_group = deque()
    nodes_to_append_to_group.append(start)
    visited = set()
    while len(nodes_to_append_to_group):
        node = nodes_to_append_to_group.popleft()
        if node in visited:
            continue
        visited.add(node)
        group.append(node)
        neighbors = graph[node]
        for neighbor in neighbors:
            nodes_to_append_to_group.append(neighbor)

    return group


def create_groups(graph: Graph) -> tuple[list[Node], list[Node]]:
    # Create group1
    node1 = list(graph.keys())[0]
    group1 = create_group(graph, node1)

    # Create group2
    node2 = [n for n in list(graph.keys()) if n not in group1][0]
    group2 = create_group(graph, node2)

    assert len(group1) + len(group2) == len(graph.keys()), "The union of both groups doesn't contain all nodes !!"

    return group1, group2


def part_one(data: str) -> int:
    graph = parse_data(data)

    # Run Monte Carlo: select n pairs and find the shortest path.
    # Record which edges get traversed most times -> these should be the edges to cut
    # (The more runs, the more likely it is to be correct)
    edges_traversed = {}
    for monte_carlo_simulation in range(200):
        if monte_carlo_simulation % 50 == 0:
            print("Running Monte-Carlo simulation", monte_carlo_simulation, "/ 200 ...")
        node1, node2 = random.sample(list(graph.keys()), 2)
        # print("node1, node2", node1, node2)
        path = get_shortest_path(graph, node1, node2)
        for i in range(len(path) - 1):
            edge = (path[i], path[i + 1]) if path[i] < path[i + 1] else (path[i + 1], path[i])
            edges_traversed[edge] = edges_traversed.get(edge, 0) + 1
    # print(edges_traversed)

    # Find edges to cut
    edges_to_cut = sorted(edges_traversed, key=lambda x: edges_traversed[x], reverse=True)[:3]
    print("edges_to_cut", edges_to_cut)

    # Recreate groups without removed nodes:
    for node1, node2 in edges_to_cut:
        graph[node1].remove(node2)
        graph[node2].remove(node1)
    group1, group2 = create_groups(graph)

    return len(group1) * len(group2)


if __name__ == "__main__":
    # ---- TEST DATA -----
    test_data = r"""jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr"""
    print("-- Tests on test data:")
    print(part_one(test_data) == 54)

    # ---- REAL DATA ----
    data = read_data("./2023/data/day25-input.txt")

    # Solution for part A
    print("\n-- Solution for part A:")
    print(part_one(data))  # 545528
    # About 2 minutes to execute (because of the Monte Carlo run 200 times)
