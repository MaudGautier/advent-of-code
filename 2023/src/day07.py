def read_data(file_name):
    with open(file_name, 'r') as file:
        return [line.strip() for line in file.readlines()]


Card = tuple[str, int]
Groups = dict[str, list[Card]]


def parse_cards(data: list[str]) -> list[Card]:
    cards = []
    for line in data:
        card, bid = line.split(" ")
        cards.append((card, int(bid)))

    return cards


def categorize(hand: str) -> str:
    counts = sorted([hand.count(i) for i in set(hand)], reverse=True)
    if counts[0] == 5:
        return "five_kind"
    if counts[0] == 4:
        return "four_kind"
    if counts[0] == 3 and counts[1] == 2:
        return "full_house"
    if counts[0] == 3:
        return "three_kind"
    if counts[0] == 2 and counts[1] == 2:
        return "two_pairs"
    if counts[0] == 2:
        return "one_pair"
    return "high_card"


def group_cards(cards: list[Card]) -> Groups:
    groups = {
        "five_kind": [],
        "four_kind": [],
        "full_house": [],
        "three_kind": [],
        "two_pairs": [],
        "one_pair": [],
        "high_card": [],
    }
    for card in cards:
        group = categorize(card[0])
        groups[group].append(card)

    return groups


def map_sort(hand: str):
    return (hand.replace("A", "a")
            .replace("K", "b", )
            .replace("Q", "c")
            .replace("J", "d")
            .replace("T", "e")
            .replace("9", "f")
            .replace("8", "g")
            .replace("7", "h")
            .replace("6", "i")
            .replace("5", "j")
            .replace("4", "k")
            .replace("3", "l")
            .replace("2", "m")
            )


def rank_cards(cards: list[Card]) -> list[Card]:
    if len(cards) <= 1:
        return cards

    return sorted(cards, key=lambda x: map_sort(x[0]), reverse=True)


def rank(groups: Groups) -> list[Card]:
    ranked_cards = []

    ranked_cards += rank_cards(groups["high_card"])
    ranked_cards += rank_cards(groups["one_pair"])
    ranked_cards += rank_cards(groups["two_pairs"])
    ranked_cards += rank_cards(groups["three_kind"])
    ranked_cards += rank_cards(groups["full_house"])
    ranked_cards += rank_cards(groups["four_kind"])
    ranked_cards += rank_cards(groups["five_kind"])

    return ranked_cards


def part_one(data: list[str]):
    cards = parse_cards(data)
    groups = group_cards(cards)
    ranked_cards = rank(groups)
    total = 0
    for r, card in enumerate(ranked_cards):
        total += card[1] * (r + 1)
    return total


if __name__ == "__main__":
    # ---- TEST DATA -----
    test_data = [
        "32T3K 765",
        "T55J5 684",
        "KK677 28",
        "KTJJT 220",
        "QQQJA 483"
    ]
    print("-- Tests on test data:")
    print(part_one(test_data) == 6440)
    # print(part_two(test_data) == 71503)

    # ---- REAL DATA ----
    data = read_data("./2023/data/day07-input.txt")

    # Solution for part A
    print("\n-- Solution for part A:")
    print(part_one(data))  # 249483956
    #
    # # Solution for part B
    # print("\n-- Solution for part B:")
    # print(part_two(data))  # 30565288
