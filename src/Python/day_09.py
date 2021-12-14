from aoc import Point, get_lines, get_neighbours_4
from functools import reduce
from typing import List, Set


def parse_input(lines: List[str]) -> List[List[int]]:
    return [[int(x) for x in line.strip()] for line in lines]


def part_1(grid: List[List[int]]) -> (int, List[Point]):
    low_points = []
    p_max = Point(len(grid[0]), len(grid))
    for y, line in enumerate(grid):
        for x, val in enumerate(line):
            if from_grid(Point(x, y), grid) < min([from_grid(p, grid) for p in get_neighbours_4(Point(x, y), p_max)]):
                low_points.append(Point(x, y))
    return sum(from_grid(p, grid) for p in low_points) + len(low_points), low_points


def part_2(grid: List[List[int]], low_points: List[Point]) -> int:
    visited = set()
    basin_size = []
    for lp in low_points:
        (lambda x: basin_size.append(len(x)) or visited.update(x))(find_basin(lp, grid, visited))
    return reduce(lambda acc, x: acc * x, sorted(basin_size, reverse=True)[0:3], 1)


def from_grid(p: Point, grid: List[List[int]]) -> int:
    return grid[p.y][p.x]


def find_basin(lp: Point, grid: List[List[int]], visited: Set[Point]) -> Set[Point]:
    basin_set = set()
    basin_set.add(lp)
    queue = [lp]
    p_max = Point(len(grid[0]), len(grid))
    while len(queue) > 0:
        for p in set(get_neighbours_4(queue.pop(), p_max)) - basin_set - visited:
            if from_grid(p, grid) != 9:
                queue.append(p)
                basin_set.add(p)
    return basin_set


def main():
    lines = get_lines("input_09.txt")
    grid = parse_input(lines)
    result, low_points = part_1(grid)
    print("Part 1:", result)  # 491
    print("Part 2:", part_2(grid, low_points))  # 1075536


if __name__ == '__main__':
    main()
