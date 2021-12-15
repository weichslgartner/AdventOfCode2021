from collections import defaultdict
from heapq import heappush, heappop
from sys import maxsize
from typing import List

from aoc import get_lines, Point, get_neighbours_4, from_grid, manhattan_distance

grid_cache = {}


def parse_input(lines: List[str]) -> List[List[int]]:
    return [[int(x) for x in line.strip()] for line in lines]


def part_1(grid: List[List[int]]) -> int:
    return a_star(Point(len(grid[0]), len(grid)), grid)


def part_2(grid: List[List[int]]) -> int:
    return a_star(Point(len(grid[0] * 5), len(grid) * 5), grid)


def from_big_grid(p: Point, grid: List[List[int]]) -> int:
    if p in grid_cache:
        return grid_cache[p]
    p_small = Point(p.x % len(grid[0]), p.y % len(grid))
    p_offset = Point(p.x // len(grid[0]), p.y // len(grid))
    v = from_grid(p_small, grid) + p_offset.x + p_offset.y
    grid_cache[p] = v - 9 if v > 9 else v
    return grid_cache[p]


def a_star(p_max: Point, grid: List[List[int]]) -> int:
    p_target = Point(p_max.x - 1, p_max.y - 1)
    start = Point(0, 0)
    queue = [(0, start)]
    in_queue = {start}
    costs = defaultdict(lambda: maxsize)
    f_costs = defaultdict(lambda: maxsize)
    costs[start] = 0
    f_costs[start] = manhattan_distance(start, p_target)
    while len(queue) > 0:
        _, cur = heappop(queue)
        in_queue.remove(cur)
        if cur == p_target:
            return costs[cur]
        for n in get_neighbours_4(cur, p_max):
            t_costs = costs[cur] + from_big_grid(n, grid)
            if t_costs < costs[n]:
                costs[n] = t_costs
                f_costs[n] = t_costs + manhattan_distance(n, p_target)
                if n not in in_queue:
                    heappush(queue, (f_costs[n], n))
                    in_queue.add(n)
    return -1


def main():
    lines = get_lines("input_15.txt")
    grid = parse_input(lines)
    print("Part 1:", part_1(grid))
    print("Part 2:", part_2(grid))


if __name__ == '__main__':
    main()
