from collections import defaultdict
from pathlib import Path

costs = {')': 3,
         ']': 57,
         '}': 1197,
         '>': 25137}


def parse_input(lines):
    return lines


def part_1(lines):
    brackets = {')': '(', ']': '[', '>': '<', '}': '{'}  # {'(': ')', '[': ']', '<': '>', '{': '}'}

    return sum(eval_line(brackets, line) for line in lines)


def eval_line(brackets, line):
    open_chunk = defaultdict(list)
    for pos, c in enumerate(line):
        if c in brackets.values():
            open_chunk[c].append(pos)
        else:
            if len(open_chunk[brackets[c]]) == 0:
               # print(f"illegal {c} in line {line}")
                return costs[c]
            else:
                open_pos = open_chunk[brackets[c]].pop()
                for o in open_chunk.values():
                    if len(o) > 0 and open_pos < o[-1]:
                       # print(f"illegal {c} in line {line}")
                        return costs[c]
    return 0


def part_2(lines):
    pass


def main():
    file = Path(__file__).parents[2] / "inputs" / "input_10.txt"
    with file.open('r') as f:
        lines = f.read().splitlines()
    lines = parse_input(lines)
    print("Part 1:", part_1(lines))
    print("Part 2:", part_2(lines))


if __name__ == '__main__':
    main()
