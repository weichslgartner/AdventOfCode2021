from pathlib import Path
from collections import Counter
from typing import List


def part_1(lines: List[str]) -> int:
    counts = [Counter(col) for col in zip(*lines)]
    gamma = int(''.join(map(lambda count: '1' if count['1'] > count['0'] else "0", counts)), 2)
    return gamma * (invert(gamma, len(lines[0])))


def invert(number: int, length: int) -> int:
    return ~number & (2 ** length - 1)


def part_2(lines: List[str]) -> int:
    return bit_select(lines, True) * bit_select(lines, False)


def bit_select(lines: List[str], keep_most_common: bool) -> int:
    for i in range(len(lines[0])):
        if len(lines) == 1:
            break
        count = Counter(list(zip(*lines))[i])
        if count['1'] == count['0']:
            keep = '1'
        elif count['1'] > count['0']:
            keep = '1'
        else:
            keep = '0'
        # invert
        if not keep_most_common:
            keep = '1' if keep == '0' else '0'
        lines = [line for line in lines if line[i] == keep]
    assert (len(lines) == 1)
    return int(lines[0], 2)


def main():
    file = Path(__file__).parents[2] / "inputs" / "input_03.txt"
    with file.open('r') as f:
        lines = f.read().splitlines()
    print("Part 1 :", part_1(lines))
    print("Part 2 :", part_2(lines))


if __name__ == '__main__':
    main()
