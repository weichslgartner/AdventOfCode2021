from typing import List

from aoc import get_lines


def parse_input(lines: List[str]) -> List[int]:
    return [int(i) for i in lines]


def part_1(numbers: List[int]) -> int:
    return sum(cur > prev for cur, prev in zip(numbers[1:], numbers[:-1]))


def part_2(numbers: List[int], window_size: int) -> int:
    return part_1([sum(x) for x in zip(*[numbers[i:] for i in range(window_size)])])


def main():
    lines = get_lines("input_01.txt")
    numbers = parse_input(lines)
    print("Part 1 :", part_1(numbers))
    print("Part 2 :", part_2(numbers, window_size=3))


if __name__ == '__main__':
    main()
