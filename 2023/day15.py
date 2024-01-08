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


Lens = tuple[str, int]
Box = list[Lens]


def run_hashmap(commands: list[str]) -> list[Box]:
    boxes = [[] for i in range(256)]
    for command in commands:
        if "=" in command:
            label = command.split("=")[0]
            focal_length = int(command.split("=")[1])
            new_lens = (label, focal_length)
            box_id = run_hash(label)
            box = boxes[box_id]
            for i, lens in enumerate(box):
                if lens[0] == label:
                    box[i] = (label, focal_length)
                    break
            else:
                boxes[box_id].append(new_lens)
        elif "-" in command:
            label = command.split("-")[0]
            box_id = run_hash(label)
            box = boxes[box_id]
            for i, lens in enumerate(box):
                if lens[0] == label:
                    del box[i]

    return boxes


def compute_focusing_power(boxes: list[Box]) -> int:
    focusing_power = 0
    for box_id, box in enumerate(boxes):
        for lens_id, lens in enumerate(box):
            focal_length = lens[1]
            focusing_power += (box_id + 1) * (lens_id + 1) * focal_length
    return focusing_power


def part_two(data: str) -> int:
    commands = parse_commands(data)
    boxes = run_hashmap(commands)
    return compute_focusing_power(boxes)


if __name__ == "__main__":
    # ---- TEST DATA -----
    test_data = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"
    print("-- Tests on test data:")
    print(run_hash("H") == 200)
    print(run_hash("HA") == 153)
    print(run_hash("HAS") == 172)
    print(run_hash("HASH") == 52)
    print(part_one(test_data) == 1320)
    print(part_two(test_data) == 145)

    # ---- REAL DATA ----
    data = read_data("./data/2023/day15-input.txt")

    # Solution for part A
    print("\n-- Solution for part A:")
    print(part_one(data))  # 514025

    # Solution for part B
    print("\n-- Solution for part B:")
    print(part_two(data))  # 244461
