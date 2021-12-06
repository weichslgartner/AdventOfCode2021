from pathlib import Path
from collections import defaultdict, Counter


def parse_input(lines):
    return [[int(i) for i in line.split(",")] for line in lines][0]


def part_1(lines, rounds):
    numbers = {}
    for i in range(rounds):
        to_add = lines.count(0)
        lines = list(map(lambda x: x-1 if x > 0 else 6,lines))
        for _ in range(to_add):
            lines.append(8)
        print(len(lines),end=",")
        print(Counter(lines))

    print(lines)
    return len(lines)


def solve(lines, rounds):
    numbers = defaultdict(int)
    for num in lines:
        numbers[num] +=1
    to_add = None
    for i in range(rounds):
        if 0 in numbers:
            to_add =  numbers[0]
        new_numbers = defaultdict(int)
        for key,values in numbers.items():
            if key >0:
                new_numbers[key-1] += values
            else:
                new_numbers[6] += values
        if to_add:
            new_numbers[8] = to_add
        to_add = None
        numbers = new_numbers
    return sum(numbers.values())


def part_2(lines):
    pass


def main():
    file = Path(__file__).parents[2] / "inputs" / "input_06.txt"
    with file.open('r') as f:
        lines = f.read().splitlines()
    lines = parse_input(lines)
    print("Part 1:", solve(lines,80))
    print("Part 2:", solve(lines,256))



if __name__ == '__main__':
    main()
