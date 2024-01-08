from collections import deque
from math import lcm
from typing import Optional


def read_data(file_name):
    with open(file_name, 'r') as file:
        return file.read().strip()


Module = str
Modules = dict[Module, tuple[str, list[Module]]]
Flipflops = dict[Module, bool]
Conjunctions = dict[Module, dict[Module, bool]]


def parse_data(data: str) -> Modules:
    modules = {}
    for line in data.split("\n"):
        raw_emitter, raw_receivers = line.split(" -> ")
        receivers = raw_receivers.split(", ")
        emitter = raw_emitter[1:]
        if raw_emitter == "broadcaster":
            modules[raw_emitter] = (raw_emitter[0], receivers)
        else:
            modules[emitter] = (raw_emitter[0], receivers)
        for receiver in receivers:
            if receiver not in modules:
                modules[receiver] = (None, [])
    return modules


def reset(modules: Modules) -> tuple[Flipflops, Conjunctions]:
    flipflops = {key: False for key, value in modules.items() if value[0] == "%"}

    conjunctions = {key: {} for key, value in modules.items() if value[0] == "&"}
    for emitter, receivers in modules.items():
        for receiver in receivers[1]:
            if receiver in conjunctions:
                conjunctions[receiver][emitter] = False

    return flipflops, conjunctions


def run(modules: Modules, flipflops: Flipflops, conjunctions: Conjunctions, receives_low_pulse: Optional[str] = None):
    high_pulses = 0
    low_pulses = 0
    queue = deque()
    queue.append(("broadcaster", False, "button"))  # module, pulse, previous_module
    while len(queue) > 0:
        current_module, pulse, previous_emitter = queue.popleft()
        kind, receivers = modules[current_module]

        # NB: This works only because all 4 modules prior to -> jq -> rx have only 1 single origin
        if receives_low_pulse and current_module == receives_low_pulse and not pulse:
            return True

        # Debug
        # print(previous_emitter, "-", "high" if pulse else "low", "->", current_module)

        # Update pulses
        if pulse:
            high_pulses += 1
        else:
            low_pulses += 1

        # Get next signals
        if kind == "b":
            # Broadcast module:  When it receives a pulse, it sends the same pulse to all of its destination modules.
            for receiver in receivers:
                queue.append((receiver, pulse, current_module))
        elif kind == "%":
            # If a flip-flop module receives a high pulse, it is ignored and nothing happens
            if pulse:
                continue
            # However, if a flip-flop module receives a low pulse, it flips between on and off.
            if not pulse:
                flipflops[current_module] = not flipflops[current_module]
                for receiver in receivers:
                    queue.append((receiver, flipflops[current_module], current_module))
        elif kind == "&":
            # When a pulse is received, the conjunction module first updates its memory for that input
            conjunctions[current_module][previous_emitter] = pulse
            # Then, if it remembers high pulses for all inputs, it sends a low pulse; otherwise, it sends a high pulse.
            # print(current_module, conjunctions, [p for p in conjunctions[current_module].values()])
            if all([p for p in conjunctions[current_module].values()]):
                for receiver in receivers:
                    queue.append((receiver, False, current_module))
            else:
                for receiver in receivers:
                    queue.append((receiver, True, current_module))

    # print("high", high_pulses, "low", low_pulses)
    return high_pulses, low_pulses


def part_one(data: str) -> int:
    modules = parse_data(data)
    flipflops, conjunctions = reset(modules)
    # high, low = run(modules, flipflops, conjunctions)
    # print(high, low, "\n\n---")
    # high, low = run(modules, flipflops, conjunctions)
    # print(high, low, "\n\n---")
    # high, low = run(modules, flipflops, conjunctions)
    # print(high, low, "\n\n---")
    # high, low = run(modules, flipflops, conjunctions)
    # print(high, low, "\n\n---")
    # high, low = run(modules, flipflops, conjunctions)
    # print(high, low, "\n\n---")

    high_pulses, low_pulses = 0, 0
    for i in range(1000):
        high, low = run(modules, flipflops, conjunctions)
        high_pulses += high
        low_pulses += low

    # print(high_pulses, low_pulses)
    return low_pulses * high_pulses


def find_high_pulse_period(data: str, module_name: str):
    modules = parse_data(data)
    flipflops, conjunctions = reset(modules)
    i = 0
    while True:
        i += 1
        output = run(modules, flipflops, conjunctions, receives_low_pulse=module_name)
        if output is True:
            return i


def find_emitters(modules: Modules, module_name: Module) -> list[Module]:
    emitters = []
    for emitter, raw_receivers in modules.items():
        if module_name in raw_receivers[1]:
            emitters.append(emitter)

    return emitters


def part_two(data: str) -> int:
    modules = parse_data(data)
    rx_emitter = find_emitters(modules, "rx")[0]
    previous_emitters = find_emitters(modules, rx_emitter)

    periods = []
    for emitter in previous_emitters:
        period = find_high_pulse_period(data, emitter)
        periods.append(period)
    # i = find_high_pulse_period(data, "vr")
    # j = find_high_pulse_period(data, "nl")
    # k = find_high_pulse_period(data, "gt")
    # l = find_high_pulse_period(data, "lr")

    return lcm(*periods)


if __name__ == "__main__":
    # ---- TEST DATA -----
    test_data_1 = r"""broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a"""
    test_data_2 = r"""broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output"""
    print("-- Tests on test data:")
    print(part_one(test_data_1) == 32000000)
    print(part_one(test_data_2) == 11687500)

    # ---- REAL DATA ----
    data = read_data("./data/2023/day20-input.txt")

    # Solution for part A
    print("\n-- Solution for part A:")
    print(part_one(data))  # 912199500

    # Solution for part B
    print("\n-- Solution for part B:")
    print(part_two(data))  # 237878264003759
