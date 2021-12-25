from typing import List, Set

from aoc import get_lines, Point


def parse_input(lines: List[str]) -> (Set[Point], Set[Point], Point):
    east_cu = set()
    down_cu = set()
    if len(lines[-1]) == 0:
        lines.pop()
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == '>':
                east_cu.add(Point(x, y))
            elif c == 'v':
                down_cu.add(Point(x, y))
    return east_cu, down_cu, Point(len(lines[0]), len(lines))


def get_east_neighbor(cu: Point, max_point: Point) -> Point:
    return Point((cu.x + 1) % max_point.x, cu.y)


def get_south_neighbor(cu: Point, max_point: Point) -> Point:
    return Point(cu.x, (cu.y + 1) % max_point.y)


def print_sea(east_cu: Set[Point], down_cu: Set[Point], max_point: Point):
    for y in range(max_point.y):
        for x in range(max_point.x):
            if Point(x, y) in east_cu:
                print(">", end="")
            elif Point(x, y) in down_cu:
                print("v", end="")
            else:
                print(".", end="")
        print()


def part_1(east_cu: Set[Point], down_cu: Set[Point], max_point: Point) -> int:
    can_move = True
    i = 0
    while can_move:
        to_move_east = set()
        for cu in east_cu:
            p = get_east_neighbor(cu, max_point)
            if p not in east_cu and p not in down_cu:
                to_move_east.add(cu)
        if to_move_east != set():
            east_cu -= to_move_east
            east_cu |= {get_east_neighbor(c, max_point) for c in to_move_east}
        to_move_south = set()
        for cu in down_cu:
            p = get_south_neighbor(cu, max_point)
            if p not in east_cu and p not in down_cu:
                to_move_south.add(cu)
        if to_move_south != set():
            down_cu -= to_move_south
            down_cu |= {get_south_neighbor(c, max_point) for c in to_move_south}
        if to_move_south == set() and to_move_east == set():
            can_move = False
        i += 1
    return i


def main():
    assert get_east_neighbor(Point(9, 0), Point(10, 9)) == Point(0, 0)
    assert get_south_neighbor(Point(9, 8), Point(10, 9)) == Point(9, 0)
    lines = get_lines("input_25.txt")
    east_cu, down_cu, max_point = parse_input(lines)
    print("Part 1:", part_1(east_cu, down_cu, max_point))


if __name__ == '__main__':
    main()
