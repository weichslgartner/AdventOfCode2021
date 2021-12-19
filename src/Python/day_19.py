from collections import defaultdict
from itertools import combinations, product, permutations
from math import sqrt

from aoc import get_lines, Point3


def rotate_x(x, y, z):
    return x, list(map(lambda n: -n,z)), y


def rotate_y(x, y, z):
    return list(map(lambda n: -n,z)), y, x

def flip(x, y, z):
    return x, list(map(lambda n: -n, y)), z

def rotate_z(x, y, z):
    return y, list(map(lambda n: -n,x)), z


def distance(a, b):
    return sum(map(lambda x: abs(x[0] - x[1]), zip(a, b)))


def euclid_distance(a, b):
    return sqrt(sum(map(lambda x: pow(x[0] - x[1], 2), zip(a, b))))


def to_point(plist):
    if len(plist) == 3:
        return Point3(plist[0], plist[1], plist[2])


def point_to_list(p):
    return [p.x,p.y,p.z]


def parse_input(lines):
    scanners = {}
    cur_scanner = []
    i = 0
    lines.append("")
    for line in lines:
        if line.startswith("---"):
            continue
        elif len(line) == 0 and len(cur_scanner) > 0:
            scanners[i] = cur_scanner
            cur_scanner = []
            i += 1
        else:
            cur_scanner.append([int(t) for t in line.split(",")])
    return scanners


def part_1(scanners):
    intersects = get_intersections(scanners)
    print(intersects)
    for i in intersects:
        p2dist1 = defaultdict(set)
        dist2p1 = defaultdict(list)
        for p in combinations(scanners[i[0]], 2):
            dist = euclid_distance(*p)
            p2dist1[to_point(p[0])].add(dist)
            p2dist1[to_point(p[1])].add(dist)
            dist2p1[dist].append(p)
        p2dist2 = defaultdict(set)
        dist2p2 = defaultdict(list)

        for p in combinations(scanners[i[1]], 2):
            dist = euclid_distance(*p)
            p2dist2[to_point(p[0])].add(dist)
            p2dist2[to_point(p[1])].add(dist)
            dist2p2[dist].append(p)
        points_a = []
        points_b = []

        for p in product(p2dist1.keys(), p2dist2.keys()):
            intersect = p2dist1[p[0]].intersection(p2dist2[p[1]])
            if len(intersect) > 1:
                points_a.append(point_to_list(p[0]))
                points_b.append(point_to_list(p[1]))
        a_transpose = list(zip(*points_a))
        b_transpose = list(zip(*points_b))
        tmp = flip(*b_transpose)
        # for _ in range(5):
        #     b_transpose = rotate_z(*b_transpose)
        #     for _ in range(5):
        #         b_transpose = rotate_y(*b_transpose)
        #         for _ in range(5):
        #             b_transpose = rotate_x(*b_transpose)
        #             found = True
        found = True
        for p in zip(tmp,a_transpose):
            print(set([x[0]+x[1] for x in zip(p[0],p[1])]))
            found =found and len(set([x[0]+x[1] for x in zip(p[0],p[1])])) ==1
        if found:
            print("Yeaf")
    # print(p2dist1)
    # print(p2dist2)


def get_intersections(scanners):
    intersections = []
    for i in combinations(range(len(scanners)), 2):
        a = set(euclid_distance(*p) for p in combinations(scanners[i[0]], 2))
        b = set(euclid_distance(*p) for p in combinations(scanners[i[1]], 2))
        if len(a.intersection(b)) == 66:
            intersections.append(i)
    return intersections


def part_2(scanners):
    pass


def main():
    lines = get_lines("input_19_test1.txt")
    scanners = parse_input(lines)
    print(scanners)
    print("Part 1:", part_1(scanners))
    print("Part 2:", part_2(scanners))


if __name__ == '__main__':
    main()
