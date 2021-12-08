from collections import defaultdict
from pathlib import Path


def parse_input(lines):
    lefts = []
    rights = []
    for line in lines:
        left, right = line.split("|")
        lefts.append(left.strip().split(" "))
        rights.append(right.strip().split(" "))
    return lefts, rights


def part_1(lines):
    cnt = 0
    for line in lines:
        for token in line:
            if len(token) == 2 or len(token) == 4 or len(token) == 3 or len(token) == 7:
                cnt += 1
    return cnt


def part_2(lefts, rights):
    numsum = 0
    for left, right in zip(lefts, rights):
        number = 0
        seg2digits = find_encoding(left)
        for token in right:
            number *= 10
            number += seg2digits[''.join(sorted(token))]
        numsum += number
    return numsum


def find_encoding(left):
    seg2digits = {}
    lendict = defaultdict(list)
    for x, y in zip(map(len, left), left):
        lendict[x].append(y)
    seg2digits[''.join(sorted(lendict[2][0]))] = 1
    seg2digits[''.join(sorted(lendict[4][0]))] = 4
    seg2digits[''.join(sorted(lendict[3][0]))] = 7
    seg2digits[''.join(sorted(lendict[7][0]))] = 8
    digits2seg = {v: k for k, v in seg2digits.items()}
    for v in lendict[6]:
        if set(digits2seg[4]).issubset(set(v)):
            seg2digits[''.join(sorted(v))] = 9
        elif not set(digits2seg[7]).issubset(set(v)):
            seg2digits[''.join(sorted(v))] = 6
        else:
            seg2digits[''.join(sorted(v))] = 0
    for v in lendict[5]:
        if set(digits2seg[1]).issubset(set(v)):
            seg2digits[''.join(sorted(v))] = 3
        elif len(set(digits2seg[4]).intersection(set(v))) == 3:
            seg2digits[''.join(sorted(v))] = 5
        else:
            seg2digits[''.join(sorted(v))] = 2
    return seg2digits


def main():
    file = Path(__file__).parents[2] / "inputs" / "input_08.txt"
    with file.open('r') as f:
        lines = f.read().splitlines()
    left, output = parse_input(lines)
    print("Part 1:", part_1(output))
    print("Part 2:", part_2(left, output))


if __name__ == '__main__':
    main()
