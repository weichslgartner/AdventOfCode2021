from aoc import get_lines
from sys import maxsize
from functools import lru_cache
from typing import List, Callable


def parse_input(lines: List[str]) -> List[int]:
    return [int(i) for i in lines[0].split(",")]


def part_1(lines: List[int]) -> int:
    return solve(lines, lambda x: x)


def part_2(lines: List[int]) -> int:
    return solve(lines, dist)


@lru_cache(4000)
def dist(x: int) -> int:
    return (x * (x + 1)) >> 1


def solve(lines: List[int], dis_fun: Callable[[int], int]) -> int:
    min_fuel = maxsize
    prev_dist = maxsize
    for i in range(min(lines), max(lines)):
        distance = sum(map(lambda x: dis_fun(abs(x - i)), lines))
        if distance > prev_dist:
            break
        min_fuel = min(min_fuel, distance)
        prev_dist = distance
    return min_fuel


def main():
    lines = get_lines("input_07.txt")
    lines = parse_input(lines)
    print("Part 1:", part_1(lines))
    print("Part 2:", part_2(lines))


if __name__ == '__main__':
    main()
