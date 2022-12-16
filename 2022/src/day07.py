def read_data(file_name):
    with open(file_name, 'r') as file:
        return [line.strip() for line in file.readlines()]


def initialise_empty_folder(tree_of_folders, path, value):
    for folder in path[:-1]:
        tree_of_folders = tree_of_folders[folder]
    tree_of_folders[path[-1]] = value


def append_file_to_folder(tree_of_folders, path, entry, value):
    for folder in path[:-1]:
        tree_of_folders = tree_of_folders[folder]
    tree_of_folders[path[-1]][entry] = value


# Structure:
# { "/":
#   {
#    "a": {},
#    "b.txt": 14848514,
#    "c.txt": 8504156,
#    "d":
#    {
#     "e": {},
#     "f": 29116,
#     "g": 2557,
#     "h.lst": 62596,
#    },
#   }
# }
def create_tree_bis(commands):
    tree = {}
    current_path = []
    for command in commands:
        command_fields = command.split(" ")
        if command_fields[0] == "$" and command_fields[1] == "cd" and command_fields[2] != "..":
            current_folder = command_fields[2]
            current_path.append(current_folder)
        elif command_fields[0] == "$" and command_fields[1] == "cd" and command_fields[2] == "..":
            current_path.pop()
        elif command_fields[0] == "$" and command_fields[1] == "ls":
            initialise_empty_folder(tree, current_path, {})
        elif command_fields[0] != "$" and command_fields[0] == "dir":
            new_dir = command_fields[1]
            # not necessary but allows to add even an empty folder
            append_file_to_folder(tree, current_path, new_dir, {})
        elif command_fields[0] != "$" and command_fields[0] != "dir":
            new_file = command_fields[1]
            file_size = int(command_fields[0])
            append_file_to_folder(tree, current_path, new_file, file_size)
    return tree


def compute_size(node, list_nodes_below_max):
    size = 0
    for key in node:
        value = node[key]
        if type(value) == int:
            size += value
        else:
            child_node_size = compute_size(value, list_nodes_below_max)
            size += child_node_size

    if size <= 100000:
        list_nodes_below_max.append(size)
    return size


def part_one(data):
    tree = create_tree_bis(data)
    list_nodes_below_max = []
    dir_size = compute_size(tree, list_nodes_below_max)
    return sum(list_nodes_below_max)


if __name__ == "__main__":
    # ---- TEST DATA -----
    test_data = [
        "$ cd /",
        "$ ls",
        "dir a",
        "14848514 b.txt",
        "8504156 c.dat",
        "dir d",
        "$ cd a",
        "$ ls",
        "dir e",
        "29116 f",
        "2557 g",
        "62596 h.lst",
        "$ cd e",
        "$ ls",
        "584 i",
        # "dir NEW_FOLDER_EMPTY",
        "$ cd ..",
        "$ cd ..",
        "$ cd d",
        "$ ls",
        "4060174 j",
        "8033020 d.log",
        "5626152 d.ext",
        "7214296 k"
    ]
    print("-- Tests on test data:")
    print(part_one(test_data) == 95437)

    # ---- REAL DATA ----
    data = read_data("./2022/data/day07-input.txt")

    # Solution for part 1
    print("\n-- Solution for part 1:")
    print(part_one(data))

    # # Solution for part 2
    # print("\n-- Solution for part 2:")
    # print(part_two(data))
