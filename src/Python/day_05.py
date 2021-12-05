from collections import namedtuple, defaultdict
from functools import reduce
from pathlib import Path
from typing import List


class Point(namedtuple('Point', 'x y')):
    def __repr__(self):
        return f'{self.y} {self.x}'


def to_point(p: str, sep=",") -> Point:
    p = p.split(sep)
    return Point(int(p[0]), int(p[1]))


def parse_input(lines: List[str]) -> List[List[Point]]:
    return [[to_point(p) for p in line.split('->')] for line in lines]


def calc_target(target: int, src: int) -> (int, int):
    if target < src:
        increment = -1
        target -= 1
    else:
        increment = 1
        target += 1
    return increment, target


def solve(segments: List[List[Point]], diagonals=False) -> int:
    point_dict = defaultdict(int)
    for segment in segments:
        if segment[0].x == segment[1].x:
            increment, target = calc_target(segment[1].y, segment[0].y)
            for y in range(segment[0].y, target, increment):
                p = Point(segment[1].x, y)
                point_dict[p] += 1
        elif segment[0].y == segment[1].y:
            increment, target = calc_target(segment[1].x, segment[0].x)
            for x in range(segment[0].x, target, increment):
                p = Point(x, segment[1].y)
                point_dict[p] += 1
        elif diagonals:
            increment_y, target_y = calc_target(segment[1].y, segment[0].y)
            increment_x, target_x = calc_target(segment[1].x, segment[0].x)
            for x, y in zip(range(segment[0].x, target_x, increment_x), range(segment[0].y, target_y, increment_y)):
                p = Point(x, y)
                point_dict[p] += 1
    return reduce(lambda acc, c: acc + 1 if c >= 2 else acc, point_dict.values(), 0)


def part_1(segments: List[List[Point]]) -> int:
    return solve(segments)


def part_2(segments: List[List[Point]]) -> int:
    return solve(segments, diagonals=True)


def main():
    file = Path(__file__).parents[2] / "inputs" / "input_05.txt"
    with file.open('r') as f:
        lines = f.read().splitlines()
    segments = parse_input(lines)
    print("Part 1 :", part_1(segments))
    print("Part 2 :", part_2(segments))


if __name__ == '__main__':
    main()
