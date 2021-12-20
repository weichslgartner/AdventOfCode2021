from aoc import get_lines, Point


def parse_input(lines):
    point_set = set()
    decoder = ["1" if c == '#' else '0' for c in lines[0]]
    max_x = 0
    max_y = 0
    for y, line in enumerate(lines[2:]):
        for x, c in enumerate(line):
            if c == '#':
                point_set.add(Point(x, y))
                max_x = max(x, max_x)
        max_y = max(y, max_y)
    return decoder, point_set, Point(max_x, max_y)


def get_code(p: Point, point_set, min_point, max_point, outside_val):
    b_string = ""
    for p in [Point(p.x + x, p.y + y) for y in range(-1, 2) for x in range(-1, 2)]:
        if p in point_set:
            b_string += "1"
        elif p.x < min_point.x or p.x > max_point.x or p.y < min_point.y or p.y > max_point.y:
            b_string += outside_val
        else:
            b_string += "0"
    return int(b_string, 2)


def part_1(decoder, point_set, max_point, rounds=2):
    return do_rounds(decoder, max_point, point_set, rounds)


def part_2(decoder, point_set, max_point, rounds=50):
    return do_rounds(decoder, max_point, point_set, rounds)


def do_rounds(decoder, max_point, point_set, rounds):
    min_point = Point(0, 0)
    outside_val = "0"
    for _ in range(rounds):
        new_point_set = set()
        for y in range(min_point.y - 1, max_point.y + 2):
            for x in range(min_point.y - 1, max_point.y + 2):
                p = Point(x, y)
                if decoder[get_code(p, point_set, min_point, max_point, outside_val)] == "1":
                    new_point_set.add(p)
        min_point = Point(min_point.x - 1, min_point.y - 1)
        max_point = Point(max_point.x + 1, max_point.y + 1)
        point_set = new_point_set
        outside_val = f"{decoder[int(outside_val * 9, 2)]}"
    return len(point_set)


def main():
    lines = get_lines("input_20.txt")
    decoder, pointset, max_point = parse_input(lines)
    print("Part 1:", part_1(decoder, pointset.copy(), max_point))
    print("Part 2:", part_2(decoder, pointset, max_point))


if __name__ == '__main__':
    main()
