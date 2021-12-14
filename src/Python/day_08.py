from aoc import get_lines
from collections import defaultdict
from functools import reduce
from itertools import chain
from typing import List, Dict

known_mappings = {2: 1, 4: 4, 3: 7, 7: 8}


def parse_input(lines: List[str]) -> (List[List[str]], List[List[str]]):
    signals = []
    outputs = []
    for line in lines:
        left, right = line.split("|")
        signals.append(left.strip().split(" "))
        outputs.append(right.strip().split(" "))
    return signals, outputs


def part_1(outputs: List[List[str]]) -> int:
    return sum(len(token) in known_mappings.keys() for token in chain.from_iterable(outputs))


def part_2(signals: List[List[str]], outputs: List[List[str]]) -> int:
    return sum(to_number(signal, output)
               for signal, output
               in zip(signals, outputs))


def to_number(signal: List[str], output: List[str]) -> int:
    return reduce(lambda acc, digit: acc * 10 + digit, [find_encoding(signal)[to_key(token)] for token in output])


def find_encoding(words: List[str]) -> Dict[str, int]:
    len2seg = reduce(lambda grp, x: grp[x[0]].append(x[1]) or grp, zip(map(len, words), words), defaultdict(list))
    # unique lengths
    seg2digits = {to_key(len2seg[k].pop()): v for k, v in known_mappings.items()}
    digits2seg = {v: set(k) for k, v in seg2digits.items()}
    # determine segments with length 6
    for v in len2seg[6]:
        if digits2seg[4].issubset(set(v)):
            seg2digits[to_key(v)] = 9
        elif not digits2seg[7].issubset(set(v)):
            seg2digits[to_key(v)] = 6
        else:
            seg2digits[to_key(v)] = 0
    # determine segments with length 5
    for v in len2seg[5]:
        if digits2seg[1].issubset(set(v)):
            seg2digits[to_key(v)] = 3
        elif len(digits2seg[4].intersection(set(v))) == 3:
            seg2digits[to_key(v)] = 5
        else:
            seg2digits[to_key(v)] = 2
    return seg2digits


def to_key(v: str) -> str:
    return ''.join(sorted(v))


def main():
    lines = get_lines("input_08.txt")
    left, output = parse_input(lines)
    print("Part 1:", part_1(output))
    print("Part 2:", part_2(left, output))


if __name__ == '__main__':
    main()
