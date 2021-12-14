from aoc import get_lines
from collections import defaultdict, Counter
from typing import List


def parse_input(lines: List[str]) -> List[int]:
    return [[int(i) for i in line.split(",")] for line in lines].pop()


def solve(lines: List[int], rounds: int) -> int:
    numbers = defaultdict(int)
    numbers.update(Counter(lines))
    for _ in range(rounds):
        new_numbers = defaultdict(int)
        for key, values in numbers.items():
            if key > 0:
                new_numbers[key - 1] += values
            else:
                new_numbers[6] += values
                new_numbers[8] = values
        numbers = new_numbers
    return sum(numbers.values())


def main():
    lines = get_lines("input_06.txt")
    lines = parse_input(lines)
    print("Part 1:", solve(lines, 80))
    print("Part 2:", solve(lines, 256))


if __name__ == '__main__':
    main()
