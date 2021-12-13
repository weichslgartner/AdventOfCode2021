from collections import namedtuple
from pathlib import Path
from typing import List, Set, Tuple


class Point(namedtuple('Point', 'x y')):
    def __repr__(self):
        return f'{self.y} {self.x}'


def parse_input(lines: List[str]) -> (List[Tuple[str, int]], Set[Point]):
    points = set()
    folds = []
    for line in lines:
        if line.startswith("fold"):
            tokens = line.split('=')
            folds.append((tokens[0][-1], int(tokens[1])))
        elif len(line) > 0:
            token = line.split(",")
            points.add(Point(int(token[0]), int(token[1])))
    return folds, points


def part_1(folds: List[Tuple[str, int]], points: Set[Point]) -> int:
    points = perform_folds(folds[0:1], points)
    return len(points)


def part_2(folds: List[Tuple[str, int]], points: Set[Point]):
    perform_folds(folds, points)
    print_board(points)
    return 0


def perform_folds(folds: List[Tuple[str, int]], points: Set[Point]) -> Set[Point]:
    for axis, location in folds:
        if axis == "y":
            points2fold = list(filter(lambda p: p.y > location, points))
            for point in points2fold:
                points.add(Point(point.x, location - (point.y - location)))
                points.remove(point)
        if axis == "x":
            points2fold = list(filter(lambda p: p.x > location, points))
            for point in points2fold:
                points.add(Point(location - (point.x - location), point.y))
                points.remove(point)
    return points


def print_board(points: Set[Point]) -> None:
    max_x = max(points, key=lambda p: p.x, )
    max_y = max(points, key=lambda p: p.y)
    for y in range(max_y.y + 1):
        for x in range(max_x.x + 1):
            if Point(x, y) in points:
                print("#", end="")
            else:
                print(".", end="")
        print()


def main():
    file = Path(__file__).parents[2] / "inputs" / "input_13.txt"
    with file.open('r') as f:
        lines = f.read().splitlines()
    folds, points = parse_input(lines)
    print("Part 1:", part_1(folds, points))
    print("Part 2:", part_2(folds, points))


if __name__ == '__main__':
    main()
