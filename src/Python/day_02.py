from aoc import get_lines
from itertools import accumulate
from operator import mul
from typing import Tuple, List


def parse_input(lines: List[str]) -> List[Tuple[str, int]]:
    return list(map(lambda x: (x[0], int(x[1])), map(lambda x: x.split(), lines)))


def part_1(lines: List[Tuple[str, int]]) -> int:
    x = sum(value for token, value in lines if token == "forward")
    depth = sum(value for token, value in lines if token == "down") - sum(
                value for token, value in lines if token == "up")
    return x * depth


def part_2(lines: List[Tuple[str, int]]) -> int:
    aims = map(lambda x: 0 if x[0] == 'forward' else (-x[1] if x[0] == 'up' else x[1]), lines)
    forwards = list(map(lambda x: x[1] if x[0] == 'forward' else 0, lines))
    depths = map(mul, forwards, accumulate(aims))
    return sum(depths) * sum(forwards)


def main():
    lines = get_lines("input_02.txt")
    lines = parse_input(lines)
    print("Part 1 :", part_1(lines))
    print("Part 2 :", part_2(lines))


if __name__ == '__main__':
    main()
