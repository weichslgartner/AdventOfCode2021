from collections import namedtuple
from functools import reduce
from itertools import tee, filterfalse
from pathlib import Path
from typing import List, Set, Tuple, Callable, Iterable


class Point(namedtuple('Point', 'x y')):
    def __repr__(self):
        return f'{self.y} {self.x}'


def partition(predicate: Callable, iterable: Iterable) -> (Iterable, Iterable):
    t1, t2 = tee(iterable)
    return filterfalse(predicate, t1), filter(predicate, t2)


def parse_input(lines: List[str]) -> (List[Tuple[str, int]], Set[Point]):
    fold_lines, point_lines = partition(lambda s: s[0].isdecimal(),
                                        filter(lambda l: len(l) > 0, lines))
    folds = [(tokens[0][-1], int(tokens[1])) for tokens in
             map(lambda x: x.split('='), fold_lines)]
    points = reduce(lambda acc, p: acc.add(p) or acc,
                    map(lambda tokens: Point(int(tokens[0]), int(tokens[1])),
                    map(lambda x: x.split(','), point_lines)),
                    set())
    return folds, points


def part_1(folds: List[Tuple[str, int]], points: Set[Point]) -> int:
    return len(perform_folds(folds[0:1], points))


def part_2(folds: List[Tuple[str, int]], points: Set[Point]):
    return to_string(perform_folds(folds[1:], points))


def perform_folds(folds: List[Tuple[str, int]], points: Set[Point]) -> Set[Point]:
    for axis, location in folds:
        if axis == "y":
            for point in list(filter(lambda p: p.y > location, points)):
                points.add(Point(point.x, location - (point.y - location)))
                points.remove(point)
        if axis == "x":
            for point in list(filter(lambda p: p.x > location, points)):
                points.add(Point(location - (point.x - location), point.y))
                points.remove(point)
    return points


def to_string(points: Set[Point]) -> str:
    max_x = max(points, key=lambda p: p.x)
    max_y = max(points, key=lambda p: p.y)
    image = "\n"
    for y in range(max_y.y + 1):
        for x in range(max_x.x + 1):
            if Point(x, y) in points:
                image += "█"
            else:
                image += " "
        image += "\n"
    return image


def main():
    file = Path(__file__).parents[2] / "inputs" / "input_13.txt"
    with file.open('r') as f:
        lines = f.read().splitlines()
    folds, points = parse_input(lines)
    print("Part 1:", part_1(folds, points))
    print("Part 2:", part_2(folds, points))


if __name__ == '__main__':
    main()
