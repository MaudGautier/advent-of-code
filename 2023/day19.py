from collections import deque
from math import prod


def read_data(file_name):
    with open(file_name, 'r') as file:
        return file.read().strip()


RawCondition = str
LeftOperator = str
Operand = str
RightOperator = int
Condition = tuple[LeftOperator, Operand, RightOperator]
Action = str
Workflow = tuple[list[tuple[Condition, Action]], Action]
Workflows = dict[str, Workflow]
Part = dict[str, int]


def create_condition(raw_condition: RawCondition) -> Condition:
    return raw_condition[0], raw_condition[1], int(raw_condition[2:])


def parse_data(data: str) -> tuple[Workflows, list[Part]]:
    raw_workflows, raw_parts = data.split("\n\n")

    workflows = {}
    for raw_workflow in raw_workflows.split("\n"):
        # print("raw_workflow.split({)", raw_workflow, raw_workflow.split("{"))
        name, raw_workflow_parts = raw_workflow.split("{")
        conditions_actions = [(c_a.split(":")[0], c_a.split(":")[1]) for c_a in raw_workflow_parts[:-1].split(",")[:-1]]
        default_action = raw_workflow_parts[:-1].split(",")[-1]
        processed_conditions_actions = [(create_condition(ca[0]), ca[1]) for ca in conditions_actions]
        workflows[name] = (processed_conditions_actions, default_action)

    parts = []
    for raw_part in raw_parts.split("\n"):
        ratings = raw_part[1:-1].split(",")
        part = {}
        for rating in ratings:
            name, score = rating.split("=")
            part[name] = int(score)
        parts.append(part)

    return workflows, parts


def process(part: Part, workflows: Workflows, action_name: str = "in") -> Action:
    # Base case
    if action_name == "R" or action_name == "A":
        return action_name

    # Recurse
    workflow = workflows[action_name]
    for condition, action in workflow[0]:
        letter, operator, value = condition
        if (operator == ">" and part[letter] > value) or (operator == "<" and part[letter] < value):
            return process(part, workflows, action)

    default_action = workflow[1]
    return process(part, workflows, default_action)


def part_one(data: str) -> int:
    workflows, parts = parse_data(data)
    total = 0
    for part in parts:
        action = process(part, workflows)
        if action == "A":
            total += sum(part.values())
    return total


def part_two(data: str) -> int:
    workflows, _ = parse_data(data)
    total = 0

    range_queues = deque()
    range_queues.append({
        "name": "in",
        "x": (1, 4000),
        "m": (1, 4000),
        "a": (1, 4000),
        "s": (1, 4000),
    })

    while len(range_queues) > 0:
        current = range_queues.popleft()
        # print("CURRENT", current)

        # Base case
        if current["name"] == "A":
            total += prod([current[letter][1] - current[letter][0] + 1 for letter in "xmas"])
            continue

        # Base case
        if current["name"] == "R":
            continue

        # Recurse
        workflow_name = current["name"]
        workflow = workflows[workflow_name]
        # print(workflow_name, workflow)
        for condition, action in workflow[0]:
            letter, operator, value = condition
            new_in_queue = {
                "name": action,
                "x": current["x"],
                "m": current["m"],
                "a": current["a"],
                "s": current["s"],
            }
            if operator == ">":
                new_in_queue[letter] = (value + 1, current[letter][1])
                current[letter] = (current[letter][0], value)
                range_queues.append(new_in_queue)

            elif operator == "<":
                new_in_queue[letter] = (current[letter][0], value - 1)
                current[letter] = (value, current[letter][1])
                range_queues.append(new_in_queue)

        default_action = workflow[1]
        new_in_queue = {
            "name": default_action,
            "x": current["x"],
            "m": current["m"],
            "a": current["a"],
            "s": current["s"],
        }
        range_queues.append(new_in_queue)

    return total


if __name__ == "__main__":
    # ---- TEST DATA -----
    test_data = r"""px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}"""
    print("-- Tests on test data:")
    print(part_one(test_data) == 19114)
    print(part_two(test_data) == 167409079868000)

    # ---- REAL DATA ----
    data = read_data("./2023/data/day19-input.txt")

    # Solution for part A
    print("\n-- Solution for part A:")
    print(part_one(data))  # 480738

    # Solution for part B
    print("\n-- Solution for part B:")
    print(part_two(data))  # 131550418841958
