from pathlib import Path
from collections import defaultdict, Counter
from typing import List


def parse_input(lines: List[str]) -> List[int]:
    return [[int(i) for i in line.split(",")] for line in lines][0]


def solve(lines: List[int], rounds: int) -> int:
    numbers = defaultdict(int)
    numbers.update(Counter(lines))
    to_add = None
    for _ in range(rounds):
        if 0 in numbers:
            to_add = numbers[0]
        new_numbers = defaultdict(int)
        for key, values in numbers.items():
            if key > 0:
                new_numbers[key - 1] += values
            else:
                new_numbers[6] += values
        if to_add:
            new_numbers[8] = to_add
        to_add = None
        numbers = new_numbers
    return sum(numbers.values())


def main():
    file = Path(__file__).parents[2] / "inputs" / "input_06.txt"
    with file.open('r') as f:
        lines = f.read().splitlines()
    lines = parse_input(lines)
    print("Part 1:", solve(lines, 80))
    print("Part 2:", solve(lines, 256))


if __name__ == '__main__':
    main()
