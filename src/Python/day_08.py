from collections import defaultdict
from functools import reduce
from itertools import chain
from pathlib import Path
from typing import List, Dict


def parse_input(lines: List[str]) -> (List[List[str]], List[List[str]]):
    signals = []
    outputs = []
    for line in lines:
        left, right = line.split("|")
        signals.append(left.strip().split(" "))
        outputs.append(right.strip().split(" "))
    return signals, outputs


def part_1(outputs: List[List[str]]) -> int:
    return sum(len(token) in [2, 3, 4, 7] for token in chain.from_iterable(outputs))


def to_number(signal: List[str], output: List[str]) -> int:
    return reduce(lambda acc, digit: acc * 10 + digit, [find_encoding(signal)[to_key(token)] for token in output])


def part_2(signals: List[List[str]], outputs: List[List[str]]) -> int:
    return sum(to_number(signal, output)
               for signal, output
               in zip(signals, outputs))


def find_encoding(left: List[str]) -> Dict[str, int]:
    seg2digits = {}
    len2seg = defaultdict(list)
    for x, y in zip(map(len, left), left):
        len2seg[x].append(y)
    # unique lengths
    seg2digits[to_key(len2seg[2][0])] = 1
    seg2digits[to_key(len2seg[4][0])] = 4
    seg2digits[to_key(len2seg[3][0])] = 7
    seg2digits[to_key(len2seg[7][0])] = 8
    digits2seg = {v: k for k, v in seg2digits.items()}
    # determine segments with length 6
    for v in len2seg[6]:
        if set(digits2seg[4]).issubset(set(v)):
            seg2digits[to_key(v)] = 9
        elif not set(digits2seg[7]).issubset(set(v)):
            seg2digits[to_key(v)] = 6
        else:
            seg2digits[to_key(v)] = 0
    # determine segments with length 5
    for v in len2seg[5]:
        if set(digits2seg[1]).issubset(set(v)):
            seg2digits[to_key(v)] = 3
        elif len(set(digits2seg[4]).intersection(set(v))) == 3:
            seg2digits[to_key(v)] = 5
        else:
            seg2digits[to_key(v)] = 2
    return seg2digits


def to_key(v: str) -> str:
    return ''.join(sorted(v))


def main():
    file = Path(__file__).parents[2] / "inputs" / "input_08.txt"
    with file.open('r') as f:
        lines = f.read().splitlines()
    left, output = parse_input(lines)
    print("Part 1:", part_1(output))
    print("Part 2:", part_2(left, output))


if __name__ == '__main__':
    main()
