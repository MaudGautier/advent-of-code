def read_data(file_name):
    with open(file_name, 'r') as file:
        return file.read().strip()


def parse_commands(data: str) -> list[str]:
    return data.split(",")


def run_hash(string: str) -> int:
    hash = 0
    for character in string:
        hash += ord(character)
        hash *= 17
        hash = hash % 256

    return hash



def part_one(data: str) -> int:
    commands = parse_commands(data)
    total = 0
    for command in commands:
        total += run_hash(command)

    return total



if __name__ == "__main__":
    # ---- TEST DATA -----
    test_data = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"
    print("-- Tests on test data:")
    print(run_hash("H") == 200)
    print(run_hash("HA") == 153)
    print(run_hash("HAS") == 172)
    print(run_hash("HASH") == 52)
    print(part_one(test_data) == 1320)
    # print(part_two(test_data) == 2)

    # ---- REAL DATA ----
    data = read_data("./2023/data/day15-input.txt")

    # Solution for part A
    print("\n-- Solution for part A:")
    print(part_one(data))  # 514025
    #
    # # Solution for part B
    # print("\n-- Solution for part B:")
    # print(part_two(data))  # 1066
