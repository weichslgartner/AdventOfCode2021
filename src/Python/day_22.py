from functools import reduce
from typing import List, Tuple, Set, Optional

from aoc import get_lines, Point3
import re

X_MIN = 0
X_MAX = 1
Y_MIN = 2
Y_MAX = 3
Z_MIN = 4
Z_MAX = 5

Cube = Tuple[int, int, int, int, int, int]


def parse_input(lines: List[str]) -> (List[bool], List[Cube]):
    return [True if line.startswith("on") else False for line in lines], \
           [tuple(map(int, re.findall(r"-?\d+", line))) for line in lines if len(line) > 0]


def part_1(on_off: List[bool], cubes: List[Cube]) -> int:
    return solve(on_off, cubes, True)


def part_2(on_off: List[bool], cubes: List[Cube]) -> int:
    return solve(on_off, cubes, False)


def solve(on_off: List[bool], cubes: List[Cube], max50: bool) -> int:
    cube_archive = set()
    n_turned = 0
    for turn_on, cube in zip(on_off, cubes):
        if max50 and abs(cube[0]) > 50:
            continue
        overlapped = []
        to_add = set()
        to_remove = set()
        for other in cube_archive:
            overlap = get_overlap(cube, other)
            if overlap is not None:
                to_add |= split_cubes(other, overlap)
                overlapped.append(overlap)
                to_remove.add(other)
        if turn_on:
            cube_archive.add(cube)
            vol = calc_volume(cube)
            if len(overlapped) > 0:
                for o in overlapped:
                    # check if any new cubes overlap
                    vol -= calc_volume(o)
            n_turned += vol
        else:
            if len(overlapped) > 0:
                for o in overlapped:
                    n_turned -= calc_volume(o)
        cube_archive |= to_add
        cube_archive -= to_remove
    return n_turned


def calc_volume(cube: Cube) -> int:
    return reduce(lambda acc, x: acc * x, map(lambda a: abs(a[1] - a[0]) + 1, zip(cube[:-1:2], cube[1::2])), 1)


def split_cubes(cube: Cube, sub_cube: Cube) -> Set[Cube]:
    if sub_cube == cube:
        return {cube}
    assert cube[X_MIN] <= sub_cube[X_MIN] <= cube[X_MAX]
    assert cube[X_MIN] <= sub_cube[X_MAX] <= cube[X_MAX]
    x_section = [cube[X_MIN], sub_cube[X_MIN] - 1, sub_cube[X_MIN], sub_cube[X_MAX], sub_cube[X_MAX] + 1, cube[X_MAX]]
    if x_section[1] < x_section[0]:
        x_section = x_section[2:]
    if x_section[-2] > x_section[-1]:
        x_section = x_section[:-2]
    assert cube[Y_MIN] <= sub_cube[Y_MIN] <= cube[Y_MAX]
    assert cube[Y_MIN] <= sub_cube[Y_MAX] <= cube[Y_MAX]
    y_section = [cube[Y_MIN], sub_cube[Y_MIN] - 1, sub_cube[Y_MIN], sub_cube[Y_MAX], sub_cube[Y_MAX] + 1, cube[Y_MAX]]
    if y_section[1] < y_section[0]:
        y_section = y_section[2:]
    if y_section[-2] > y_section[-1]:
        y_section = y_section[:-2]
    assert cube[Z_MIN] <= sub_cube[Z_MIN] <= cube[Z_MAX]
    assert cube[Z_MIN] <= sub_cube[Z_MAX] <= cube[Z_MAX]
    z_section = [cube[Z_MIN], sub_cube[Z_MIN] - 1, sub_cube[Z_MIN], sub_cube[Z_MAX], sub_cube[Z_MAX] + 1, cube[Z_MAX]]
    if z_section[1] < z_section[0]:
        z_section = z_section[2:]
    if z_section[-2] > z_section[-1]:
        z_section = z_section[:-2]
    cubes = set()
    for x1, x2 in zip(x_section[::2], x_section[1::2]):
        for y1, y2 in zip(y_section[::2], y_section[1::2]):
            for z1, z2 in zip(z_section[::2], z_section[1::2]):
                # don't add sub_sub to cubes
                if not (x1 == sub_cube[X_MIN] and x2 == sub_cube[X_MAX] and
                        y1 == sub_cube[Y_MIN] and y2 == sub_cube[Y_MAX] and
                        z1 == sub_cube[Z_MIN] and z2 == sub_cube[Z_MAX]):
                    cubes.add((x1, x2, y1, y2, z1, z2))
    return cubes


def get_overlap(cube1: Cube, cube2: Cube) -> Optional[Cube]:
    x_overlap = None
    y_overlap = None
    z_overlap = None
    # x overlap 1
    if max(cube1[X_MIN], cube2[X_MIN]) <= min(cube1[X_MAX], cube2[X_MAX]):
        x_overlap = (max(cube1[X_MIN], cube2[X_MIN]), min(cube1[X_MAX], cube2[X_MAX]))
    if max(cube1[Y_MIN], cube2[Y_MIN]) <= min(cube1[Y_MAX], cube2[Y_MAX]):
        y_overlap = (max(cube1[Y_MIN], cube2[Y_MIN]), min(cube1[Y_MAX], cube2[Y_MAX]))
    if max(cube1[Z_MIN], cube2[Z_MIN]) <= min(cube1[Z_MAX], cube2[Z_MAX]):
        z_overlap = (max(cube1[Z_MIN], cube2[Z_MIN]), min(cube1[Z_MAX], cube2[Z_MAX]))
    if x_overlap is not None and y_overlap is not None and z_overlap is not None:
        return x_overlap + y_overlap + z_overlap
    return None


def to_points(cube: Cube) -> Set[Point3]:
    """
    for testing only
    """
    points = set()
    for x in range(cube[0], cube[1] + 1):
        for y in range(cube[2], cube[3] + 1):
            for z in range(cube[4], cube[5] + 1):
                points.add(Point3(x, y, z))
    return points


def tests():
    """
    for testing only
    """
    assert calc_volume((10, 12, 10, 12, 10, 12)) == 27
    assert calc_volume((11, 13, 11, 13, 11, 13)) == 27
    assert calc_volume((10, 10, 10, 10, 10, 10)) == 1
    assert calc_volume((-10, -10, -10, -10, -10, -10)) == 1
    assert get_overlap((10, 10, 10, 10, 10, 10), (10, 10, 10, 10, 10, 10)) == (10, 10, 10, 10, 10, 10)
    assert get_overlap((10, 12, 10, 12, 10, 12), (11, 13, 11, 13, 11, 13)) == (11, 12, 11, 12, 11, 12)
    assert get_overlap((10, 10, 10, 10, 10, 10), (-10, -10, -10, -10, -10, -10)) is None
    assert get_overlap((10, 11, 10, 11, 10, 11), (10, 12, 10, 12, 10, 12)) == (10, 11, 10, 11, 10, 11)
    assert len(split_cubes((10, 12, 10, 12, 10, 12), sub_cube=(10, 11, 10, 11, 10, 11))) == 7
    assert len(split_cubes((10, 13, 10, 13, 10, 13), sub_cube=(11, 11, 11, 11, 11, 11))) == 26
    assert set(to_points((10, 12, 10, 12, 10, 12))).difference({Point3(11, 11, 11)}) == split_cubes(
        (10, 12, 10, 12, 10, 12), sub_cube=(11, 11, 11, 11, 11, 11))
    assert set(to_points((10, 12, 10, 12, 10, 12))).difference(to_points((10, 11, 10, 11, 10, 11))) == split_cubes(
        (10, 12, 10, 12, 10, 12), sub_cube=(10, 11, 10, 11, 10, 11))
    overlap = get_overlap((-20, 33, -21, 23, -26, 28), (-20, 26, -36, 17, -47, 7))
    assert set(to_points((-20, 26, -36, 17, -47, 7))) - to_points(overlap) == split_cubes((-20, 26, -36, 17, -47, 7),
                                                                                          sub_cube=overlap)
    assert get_overlap((-48, -32, 26, 41, -47, -37), (-46, -23, 21, 46, -50, -30)) == (-46, -23, 21, 46, -47, -37)


def cubes_to_set(cubes: List[Cube]) -> Set[Point3]:
    """
    for testing only
    """
    points = set()
    for c in cubes:
        points |= to_points(c)
    return points


def main(do_tests: bool = False):
    tests() if do_tests else None
    lines = get_lines("input_22.txt")
    cubes: List[Cube]
    on_off, cubes = parse_input(lines)
    print("Part 1:", part_1(on_off, cubes))
    print("Part 2:", part_2(on_off, cubes))


if __name__ == '__main__':
    main()
