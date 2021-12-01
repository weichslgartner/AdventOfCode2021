from pathlib import Path
from typing import List


def parse_input(lines: List[str]) -> List[int]:
    return [int(i) for i in lines]


def part_1(numbers: List[int]) -> int:
    return sum(cur > prev for cur, prev in zip(numbers[1:], numbers[:-1]))


def part_2(numbers: List[int], window_size: int) -> int:
    return part_1([sum(x) for x in zip(*[numbers[i:] for i in range(window_size)])])


def main():
    file = Path(__file__).parents[2] / "inputs" / "input_01.txt"
    with file.open('r') as f:
        lines = f.read().splitlines()
    numbers = parse_input(lines)
    print("Part 1 :", part_1(numbers))
    print("Part 2 :", part_2(numbers, window_size=3))


if __name__ == '__main__':
    main()
