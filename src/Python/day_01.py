from pathlib import Path


def parse_input(lines):
    lines = [int (i) for i in lines]
    return lines


def part_1(lines):
    larger = 0
    for i in range(1,len(lines)):
        if lines[i] > lines[i-1]:
            larger +=1
    return larger


def part_2(lines):
    larger = 0
    prev = 1111111111
    for i in range(2, len(lines)):
        if lines[i]+lines[i-1]+lines[i-2]  > prev:
            larger += 1
        prev = lines[i]+lines[i-1]+lines[i-2]
    return larger


def main():
    file = Path(__file__).parents[2] / "inputs" / f"input_01.txt"
    with file.open('r') as f:
        lines = f.read().splitlines()
    lines = parse_input(lines)
    print("Part 1 :", part_1(lines))
    print("Part 2 :", part_2(lines))


if __name__ == '__main__':
    main()
