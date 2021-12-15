import heapq
from collections import defaultdict
from sys import maxsize

from aoc import get_lines, Point, get_neighbours_4, from_grid


def parse_input(lines):
    return [[int(x) for x in line.strip()] for line in lines]


def manhattan_dist(a: Point, b: Point):
    return abs(a.x - b.x) + abs(a.y - b.y)


def get_path(cur, cameFrom, grid):
    path = [from_big_grid(cur, grid)]
    while cur in cameFrom.keys():
        cur = cameFrom[cur]
        path.append(from_big_grid(cur, grid))
        print(cur, from_big_grid(cur, grid))
    return sum(path[:-1])


def part_1(grid):
    return a_star( Point(len(grid[0]), len(grid)), grid)


def from_big_grid(p, grid):
    p_small = Point(p.x % len(grid[0]), p.y % len(grid))
    p_offset = Point(p.x // len(grid[0]), p.y // len(grid))
    v = from_grid(p_small, grid)
    v = v + p_offset.x + p_offset.y
    if v > 9:
        v -= 9
    return v


def part_2(grid):
    return a_star(Point(len(grid[0] * 5), len(grid) * 5), grid)


def a_star(p_max, grid):
    p_target = Point(p_max.x - 1, p_max.y - 1)
    start = Point(0, 0)
    q = []
    heapq.heappush(q, (0, start))
    in_queue = set()
    in_queue.add(start)
    costs = defaultdict(lambda: maxsize)
    fcosts = defaultdict(lambda: maxsize)
    costs[start] = 0
    fcosts[start] = manhattan_dist(start, p_target)
    while len(q) > 0:
        _, cur = heapq.heappop(q)
        in_queue.remove(cur)
        if cur == p_target:
            return costs[cur]
        for n in get_neighbours_4(cur, p_max):
            t_costs = costs[cur] + from_big_grid(n, grid)
            if t_costs < costs[n]:
                costs[n] = t_costs
                fcosts[n] = t_costs + manhattan_dist(n, p_target)
                if n not in in_queue:
                    heapq.heappush(q, (fcosts[n], n))
                    in_queue.add(n)
    return -1


def main():
    lines = get_lines("input_15.txt")
    grid = parse_input(lines)
    print("Part 1:", part_1(grid))
    print("Part 2:", part_2(grid))


if __name__ == '__main__':
    main()
