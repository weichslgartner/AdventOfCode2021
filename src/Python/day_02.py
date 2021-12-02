from pathlib import Path


def parse_input(lines):
    return [line.split(" ") for line in lines]


def part_1(lines):
    depth = 0
    x = 0
    for line in lines:
        if "forward" in line[0]:
            x += int(line[1])
        elif "down" in line[0]:
            depth += int(line[1])
        else:
            depth -= int(line[1])
    return x*depth


def part_2(lines):
    depth = 0
    x = 0
    aim = 0
    for line in lines:
        if "forward" in line[0]:
            x += int(line[1])
            depth += int(line[1]) * aim
        elif "down" in line[0]:
            aim += int(line[1])
        else:
            aim -= int(line[1])
    return x * depth


def main():
    file = Path(__file__).parents[2] / "inputs" / "input_02.txt"
    with file.open('r') as f:
        lines = f.read().splitlines()
    lines = parse_input(lines)
    print("Part 1 :", part_1(lines))
    print("Part 2 :", part_2(lines))


if __name__ == '__main__':
    main()
