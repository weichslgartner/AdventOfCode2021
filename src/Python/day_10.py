from collections import defaultdict
from typing import List, Dict

from aoc import get_lines


def part_1(lines: List[str]) -> int:
    return sum((lambda x: x[0])(eval_line(line)) for line in lines)


def part_2(lines: List[str]) -> int:
    costs = [eval_autocomplete_costs(open_chunk) for _, open_chunk in
             filter(lambda x: x[0] == 0, map(eval_line, lines))]
    return sorted(costs)[len(costs) // 2]


def eval_line(line: str) -> (int, Dict[str, List[int]]):
    costs_corrupt = {')': 3,
                     ']': 57,
                     '}': 1197,
                     '>': 25137}
    close2open = {')': '(', ']': '[', '>': '<', '}': '{'}
    open_chunk = defaultdict(list)
    for pos, c in enumerate(line):
        if c in close2open.values():
            open_chunk[c].append(pos)
        else:
            if len(open_chunk[close2open[c]]) == 0:
                return costs_corrupt[c], None
            else:
                open_pos = open_chunk[close2open[c]].pop()
                for o in open_chunk.values():
                    if len(o) > 0 and open_pos < o[-1]:
                        return costs_corrupt[c], None
    return 0, open_chunk


def eval_autocomplete_costs(open_chunk: Dict[str, List[int]]) -> int:
    costs_dict = {')': 1,
                  ']': 2,
                  '}': 3,
                  '>': 4}
    open2close = {'(': ')', '[': ']', '<': '>', '{': '}'}
    line_costs = 0
    while len(open_chunk) > 0:
        max_pos = -1
        max_c = ""
        for k, v, in open_chunk.items():
            if len(v) > 0 and v[-1] > max_pos:
                max_pos = v[-1]
                max_c = k
        if len(open_chunk[max_c]) > 0:
            open_chunk[max_c].pop()
            line_costs = line_costs * 5 + costs_dict[open2close[max_c]]
        else:
            return line_costs
    return line_costs


def main():
    lines = get_lines("input_10.txt")
    print("Part 1:", part_1(lines))
    print("Part 2:", part_2(lines))


if __name__ == '__main__':
    main()
