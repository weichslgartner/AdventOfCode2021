from collections import namedtuple
from itertools import filterfalse, tee
from pathlib import Path
from typing import List, Callable, Iterable, Iterator


class Point(namedtuple('Point', 'x y')):
    def __repr__(self):
        return f'{self.y} {self.x}'


def to_point(p: str, sep=",") -> Point:
    p = p.split(sep)
    return Point(int(p[0]), int(p[1]))


def get_neighbours_4(p: Point, p_max: Point) -> Iterator[Point]:
    points = [Point(p.x - 1, p.y), Point(p.x, p.y - 1), Point(p.x + 1, p.y), Point(p.x, p.y + 1)]
    return filter(lambda x: is_in_grid(x, p_max), points)


def get_neighbours_8(p: Point, p_max: Point) -> Iterator[Point]:
    points = [Point(p.x + x, p.y + y) for y in range(-1, 2) for x in range(-1, 2) if x != 0 or y != 0]
    return filter(lambda n: is_in_grid(n, p_max), points)


def is_in_grid(p: Point, p_max: Point) -> bool:
    return (p.x >= 0) and (p.y >= 0) and (p.x < p_max.x) and (p.y < p_max.y)


def get_lines(file_name: str) -> List[str]:
    file = Path(__file__).parents[2] / "inputs" / file_name
    with file.open('r') as f:
        lines = f.read().splitlines()
    return lines


def partition(predicate: Callable, iterable: Iterable) -> (Iterable, Iterable):
    t1, t2 = tee(iterable)
    return filterfalse(predicate, t1), filter(predicate, t2)


def line_to_int(line: str, split_char=",") -> List[int]:
    return [int(i) for i in line.split(split_char) if len(i) > 0]
