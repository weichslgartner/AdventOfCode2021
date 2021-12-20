from typing import List, Set

from aoc import get_lines, Point


def parse_input(lines: List[str]) -> (List[int], Set[Point], Point):
    decoder_raw, image_raw = lines[0], lines[2:]
    point_set = {Point(x, y) for y, line in enumerate(image_raw) for x, c in enumerate(line) if c == '#'}
    return [1 if c == '#' else 0 for c in decoder_raw], point_set, Point(len(image_raw[0]), len(image_raw))


def get_code(p: Point, point_set: Set[Point], min_point: Point, max_point: Point, outside_val: int) -> int:
    code = 0
    for i, p in enumerate([Point(p.x + x, p.y + y) for y in range(-1, 2) for x in range(-1, 2)]):
        if p in point_set:
            code |= 1 << i
        elif p.x < min_point.x or p.x > max_point.x or p.y < min_point.y or p.y > max_point.y:
            code |= outside_val << i
    return code


def part_1(decoder: List[int], point_set: Set[Point], max_point: Point, rounds: int = 2) -> int:
    return do_rounds(decoder, point_set, max_point, rounds)


def part_2(decoder: List[int], point_set: Set[Point], max_point: Point, rounds: int = 50) -> int:
    return do_rounds(decoder, point_set, max_point, rounds)


def do_rounds(decoder: List[int], point_set: Set[Point], max_point: Point, rounds: int) -> int:
    min_point = Point(0, 0)
    outside_val = 0
    for _ in range(rounds):
        point_set = {Point(x, y)
                     for y in range(min_point.y - 1, max_point.y + 2)
                     for x in range(min_point.y - 1, max_point.y + 2) if
                     decoder[get_code(Point(x, y), point_set, min_point, max_point, outside_val)]}
        min_point = Point(min_point.x - 1, min_point.y - 1)
        max_point = Point(max_point.x + 1, max_point.y + 1)
        outside_val = decoder[0 if outside_val == 0 else 2 ** 9 - 1]
    return len(point_set)


def main():
    lines = get_lines("input_20.txt")
    decoder, point_set, max_point = parse_input(lines)
    print("Part 1:", part_1(decoder, point_set, max_point))
    print("Part 2:", part_2(decoder, point_set, max_point))


if __name__ == '__main__':
    main()
