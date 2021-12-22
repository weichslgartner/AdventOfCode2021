from itertools import islice
from functools import reduce

from aoc import get_lines, take, Point3
import re


def calc_volume(points):
    return reduce(lambda acc, x: acc * x, map(lambda a: abs(a[1] - a[0]) + 1, zip(points[:-1:2], points[1::2])), 1)


def parse_input(lines):
    return [True if line.startswith("on") else False for line in lines], [list(map(int, re.findall(r"-?\d+", line))) for
                                                                          line in lines]


def part_1(on_off, cubes):
    points = set()
    for turn_on, cube in zip(on_off, cubes):
        if abs(cube[0]) > 50:
            continue
        cube_points = to_points(cube, points)
        if turn_on:
            points |=  cube_points
        else:
            points -=  cube_points
    return len(points)


def to_points(cube):
    points = set()
    for x in range(cube[0], cube[1] + 1):
        for y in range(cube[2], cube[3] + 1):
            for z in range(cube[4], cube[5] + 1):
                points.add(Point3(x, y, z))
    return points


def part_2(lines):
    pass


def do_overlap(cube1, cube2):
    x_overlap = None
    y_overlap = None
    z_overlap = None
    # x overlap 1
    if cube2[0] <= cube1[1] <= cube2[1]:
        x_overlap = [cube2[0], cube1[1]]
    if cube2[1] >= cube1[0] >= cube2[0]:
        x_overlap = [cube1[0], cube2[1]]


def tests():
    assert calc_volume([10, 12, 10, 12, 10, 12]) == 27
    assert calc_volume([11, 13, 11, 13, 11, 13]) == 27
    assert calc_volume([10, 10, 10, 10, 10, 10]) == 1
    assert calc_volume([-10, -10, -10, -10, -10, -10]) == 1


def main():
    tests()
    lines = get_lines("input_22.txt")
    on_off, cubes = parse_input(lines)
    print("Part 1:", part_1(on_off, cubes))
    print("Part 2:", part_2(lines))


if __name__ == '__main__':
    main()
