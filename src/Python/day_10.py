from collections import defaultdict
from pathlib import Path

costs_corrupt = {')': 3,
                 ']': 57,
                 '}': 1197,
                 '>': 25137}


def parse_input(lines):
    return lines


def part_1(lines):
    return sum((lambda x: x[0])(eval_line(line)) for line in lines)


def eval_line(line):
    brackets = {')': '(', ']': '[', '>': '<', '}': '{'}  # {'(': ')', '[': ']', '<': '>', '{': '}'}
    open_chunk = defaultdict(list)
    for pos, c in enumerate(line):
        if c in brackets.values():
            open_chunk[c].append(pos)
        else:
            if len(open_chunk[brackets[c]]) == 0:
                # print(f"illegal {c} in line {line}")
                return costs_corrupt[c], None
            else:
                open_pos = open_chunk[brackets[c]].pop()
                for o in open_chunk.values():
                    if len(o) > 0 and open_pos < o[-1]:
                        # print(f"illegal {c} in line {line}")
                        return costs_corrupt[c], None
    return 0, open_chunk


def part_2(lines):
    costs = []
    for line in lines:
        score, open_chunk = eval_line(line)
        if score > 0:
            continue
        costs.append(eval_autocomplete_costs(open_chunk))
    return sorted(costs)[len(costs) // 2]


def eval_autocomplete_costs(open_chunk):
    costs_dict = {')': 1,
                  ']': 2,
                  '}': 3,
                  '>': 4}
    brackets = {'(': ')', '[': ']', '<': '>', '{': '}'}
    line_costs = 0
    while len(open_chunk) > 0:  # ])}>
        max_pos = -1
        max_c = ""
        for k, v, in open_chunk.items():
            if len(v) > 0 and v[-1] > max_pos:
                max_pos = v[-1]
                max_c = k
        if len(open_chunk[max_c]) > 0:
            open_chunk[max_c].pop()
            line_costs = line_costs * 5 + costs_dict[brackets[max_c]]
        else:
            return line_costs
    return line_costs


def main():
    file = Path(__file__).parents[2] / "inputs" / "input_10.txt"
    with file.open('r') as f:
        lines = f.read().splitlines()
    lines = parse_input(lines)
    print("Part 1:", part_1(lines))
    print("Part 2:", part_2(lines))


if __name__ == '__main__':
    main()
