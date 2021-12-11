from collections import namedtuple
from functools import reduce
from itertools import chain
from pathlib import Path
from queue import SimpleQueue
from typing import List, Iterator, Set


class Point(namedtuple('Point', 'x y')):
    def __repr__(self):
        return f'{self.y} {self.x}'


def is_in_grid(p: Point, p_max: Point) -> bool:
    return (p.x >= 0) and (p.y >= 0) and (p.x < p_max.x) and (p.y < p_max.y)


def get_neighbours(p: Point, p_max: Point) -> Iterator[Point]:
    points = [Point(p.x + x, p.y + y) for y in range(-1, 2) for x in range(-1, 2) if x != 0 or y != 0]
    return filter(lambda n: is_in_grid(n, p_max), points)


def parse_input(lines: List[str]) -> List[List[int]]:
    return [[int(x) for x in line.strip()] for line in lines]


def part_1(grid: List[List[int]], rounds: int = 100) -> int:
    flashed_cnt = 0
    for _ in range(rounds):
        flashed_round, grid = perform_round(grid)
        flashed_cnt += flashed_round
    return flashed_cnt


def perform_round(grid: List[List[int]]) -> (int, List[List[int]]):
    p_max = Point(len(grid[0]), len(grid))
    # creates a new grid. but also saves us from deep copies
    grid = [[val + 1 for val in line] for line in grid]
    flashed = set()
    flashed_cnt = 0
    for y, line in enumerate(grid):
        for x, val in enumerate(line):
            if val > 9:
                flashed_cnt += flash_point(flashed, grid, Point(x, y))
                flashed_cnt += handle_neighbors(flashed, grid, p_max, Point(x, y))
    return flashed_cnt, grid


def flash_point(flashed: Set[Point], grid: List[List[int]], p: Point) -> int:
    grid[p.y][p.x] = 0
    flashed.add(p)
    return 1


def handle_neighbors(flashed: Set[Point], grid: List[List[int]], p_max: Point, p: Point) -> int:
    flashed_cnt = 0
    queue = SimpleQueue()
    for n in get_neighbours(p, p_max):
        queue.put(n)
    while not queue.empty():
        p = queue.get()
        if p not in flashed:
            grid[p.y][p.x] += 1
        if grid[p.y][p.x] > 9:
            flashed_cnt += flash_point(flashed, grid, p)
            for n in get_neighbours(p, p_max):
                queue.put(n)
    return flashed_cnt


def part_2(grid: List[List[int]]) -> int:
    for i in range(10000000000):
        _, grid = perform_round(grid)
        if reduce(lambda acc, y: acc and y == 0, chain.from_iterable(grid), True):
            return i + 1
    return -1


def main():
    file = Path(__file__).parents[2] / "inputs" / "input_11.txt"
    with file.open('r') as f:
        lines = f.read().splitlines()
    grid = parse_input(lines)
    print("Part 1:", part_1(grid, 100))
    print("Part 2:", part_2(grid))


if __name__ == '__main__':
    main()
