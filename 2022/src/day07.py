def read_data(file_name):
    with open(file_name, 'r') as file:
        return [line.strip() for line in file.readlines()]


# Structure:
# { "/":
#   [
#    "a": [],
#    "b.txt": 14848514,
#    "c.txt": 8504156,
#    "d":
#    [
#     "e": [],
#     "f": 29116,
#     "g": 2557,
#     "h.lst": 62596,
#    ],
#   ]
# }
def create_tree_bis(commands):
    tree = {}
    current_path = []
    for command in commands:
        command_fields = command.split(" ")
        if command_fields[0] == "$" and command_fields[1] == "cd" and command_fields[2] != "..":
            current_folder = command_fields[2]
            current_path.append(current_folder)
            # print("CDING", current_folder, "IN PATH", current_path)
        elif command_fields[0] == "$" and command_fields[1] == "cd" and command_fields[2] == "..":
            current_folder = current_path.pop()
            # print("CDING", current_folder, "IN PATH", current_path)
        elif command_fields[0] == "$" and command_fields[1] == "ls":
            print("-- READING", current_folder, "IN PATH", current_path)
        elif command_fields[0] != "$" and command_fields[0] == "dir":
            new_dir = command_fields[1]
            print("DIR", new_dir, "IS IN", current_folder, "IN PATH", current_path)
        elif command_fields[0] != "$" and command_fields[0] != "dir":
            new_file = command_fields[1]
            file_size = command_fields[0]
            print("FILE", new_file, "IS IN", current_folder, "IN PATH", current_path, "WITH SIZE", file_size)


def part_one(data):
    tree = create_tree_bis(data)
    return False


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

    # # Solution for part a
    # print("\n-- Solution for part a:")
    # print(part_one(data))
    #
    # # Solution for part b
    # print("\n-- Solution for part b:")
    # print(part_two(data))
