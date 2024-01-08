def read_data(file_name):
    with open(file_name, 'r') as file:
        return [line.strip() for line in file.readlines()]


def parse_card(card: str) -> tuple[set[int], set[int]]:
    winning_numbers, numbers_in_hands = card.split(": ")[1].split(" | ")
    winning_numbers_set = set(winning_numbers.split())
    numbers_in_hands_set = set(numbers_in_hands.split())
    return winning_numbers_set, numbers_in_hands_set


def compute_score(winning_numbers: set[int], numbers_in_hand: set[int]) -> int:
    common_numbers = winning_numbers.intersection(numbers_in_hand)
    return 2 ** (len(common_numbers) - 1) if len(common_numbers) >= 1 else 0


def part_one(data: list[str]) -> int:
    total = 0
    for card in data:
        winning_numbers, numbers_in_hand = parse_card(card)
        total += compute_score(winning_numbers, numbers_in_hand)

    return total


def part_two(data: list[str]) -> int:
    nb_copies = [1] * len(data)
    for i, card in enumerate(data):
        winning_numbers, numbers_in_hand = parse_card(card)
        common_numbers = winning_numbers.intersection(numbers_in_hand)
        for j in range(len(common_numbers)):
            copy_idx = i + 1 + j
            if copy_idx >= len(data):
                break
            nb_copies[copy_idx] += nb_copies[i]

    return sum(nb_copies)


if __name__ == "__main__":
    # ---- TEST DATA -----
    test_data = [
        "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53",
        "Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19",
        "Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1",
        "Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83",
        "Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36",
        "Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11",
    ]
    print("-- Tests on test data:")
    print(part_one(test_data) == 13)
    print(part_two(test_data) == 30)

    # ---- REAL DATA ----
    data = read_data("./data/2023/day04-input.txt")

    # Solution for part A
    print("\n-- Solution for part A:")
    print(part_one(data))  # 25183

    # Solution for part B
    print("\n-- Solution for part B:")
    print(part_two(data))  # 5667240
