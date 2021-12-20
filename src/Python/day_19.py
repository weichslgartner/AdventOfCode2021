from collections import defaultdict, deque
from itertools import combinations, product, permutations, cycle
from math import sqrt

from aoc import get_lines, Point3

rotations = [([2, 0, 1], [-1, -1, 1]), ([0, 1, 2], [1, -1, -1]), ([2, 1, 0], [-1, -1, -1]), ([2, 1, 0], [1, -1, 1]),
             ([0, 2, 1], [-1, -1, -1]), ([1, 2, 0], [1, -1, -1]), ([1, 0, 2], [-1, -1, -1]), ([1, 2, 0], [1, 1, 1]),
             ([0, 2, 1], [-1, 1, 1]), ([0, 1, 2], [-1, 1, -1]), ([0, 2, 1], [1, -1, 1]), ([2, 0, 1], [-1, 1, -1]),
             ([1, 0, 2], [1, 1, -1]), ([2, 1, 0], [1, 1, -1]), ([2, 0, 1], [1, 1, 1]), ([2, 1, 0], [-1, 1, 1]),
             ([0, 1, 2], [1, 1, 1]), ([1, 0, 2], [1, -1, 1]), ([1, 0, 2], [-1, 1, 1]), ([0, 1, 2], [-1, -1, 1]),
             ([1, 2, 0], [-1, 1, -1]), ([1, 2, 0], [-1, -1, 1]), ([0, 2, 1], [1, 1, -1]), ([2, 0, 1], [1, -1, -1])]


def rotate(l, perms, signs):
    return list(map(lambda n: n * signs[0], l[perms[0]])), list(map(lambda n: n * signs[1], l[perms[1]])), list(
        map(lambda n: n * signs[2], l[perms[2]])),


def rotate_x(x, y, z):
    return x, list(map(lambda n: -n, z)), y


def rotate_y(x, y, z):
    return list(map(lambda n: -n, z)), y, x


def flip_y(x, y, z):
    return x, list(map(lambda n: -n, y)), z


def flip_x(x, y, z):
    return list(map(lambda n: -n, x)), y, z


def flip_z(x, y, z):
    return x, y, list(map(lambda n: -n, z))


def rotate_z(x, y, z):
    return y, list(map(lambda n: -n, x)), z


def distance(a, b):
    return sum(map(lambda x: abs(x[0] - x[1]), zip(a, b)))


def euclid_distance(a, b):
    return sqrt(sum(map(lambda x: pow(x[0] - x[1], 2), zip(a, b))))


def to_point(plist):
    if len(plist) == 3:
        return Point3(plist[0], plist[1], plist[2])


def point_to_list(p):
    return [p.x, p.y, p.z]


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
    mapping_dict, perms, signs = get_relative_centers(intersects, scanners)
    print(mapping_dict)

    print(perms,signs)
    to_transform = [[160, -1134, -23]]
    trans_perm = [0, 1, 2]
    trans_sign = [-1, 1, -1]
    target_center = [68, -1246, -43]
    transform(list(zip(*to_transform)),target_center, trans_perm, trans_sign)
    transformed_scanners = set()
    beacons = set(to_point(p) for p in scanners[0]  )
    queue = deque()
    used_mappings = set()
    transformed_scanners.add(0)
    for key in mapping_dict.keys():
        if key[0] == 0:
            queue.append( key)
    while len(queue) >0:
        el = queue.popleft()
        print(el)
        p_tanspose = list(zip(*scanners[el[1]]))
        use_mapping = el
        new_points = set()
        while True:
            p_tanspose = transform(p_tanspose,*mapping_dict[use_mapping])
            new_points = set(to_point(p) for p in zip(*p_tanspose))
            if use_mapping[0] == 0:
                break
            for mapping in used_mappings:
                if mapping[1] == use_mapping[0]:
                    use_mapping = mapping
                    break


        transformed_scanners.add(el[1])
        beacons.update(new_points)
        used_mappings.add(el)
        for k in mapping_dict.keys():
            if k[0] == el[1] and k[1] not in transformed_scanners:
                queue.append(k)


        print(len(beacons))
    return len(beacons)
    #  print(list(zip(*rotated)))

  #  a_transpose = list(zip(*points_a))
   # b_transpose = list(zip(*[160, -1134, -23]))

    #list(zip(*scanners[1]))
    # for _ in range(3):
    #     b_transpose = rotate_z(*b_transpose)
    #     for _ in range(3):
    #         b_transpose = rotate_y(*b_transpose)
    #         for _ in range(8):
    #             b_transpose = rotate_x(*b_transpose)
    #
    #             offset = []
    #             for p in zip(b_transpose, a_transpose):
    #                 points = set([x[1] - x[0] for x in zip(p[0], p[1])])
    #                 if len(points) == 1:
    #                     offset.append(points.pop())
    #             if len(offset) == 3:
    #                 print(offset)

    # print(len(transforms))

    # print(b_transpose)
    # b_transpose = flip_x(*b_transpose)
    # print(b_transpose)
    # b_transpose = flip_z(*b_transpose)

    # found = found and len(set([x[1] - x[0] for x in zip(p[0], p[1])])) == 1

    # print(p2dist1)
    # print(p2dist2)


def get_relative_centers(intersects, scanners):
    mapping_dict = {}
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

        # b_transpose = list(zip(*[[0, 1, 2]]))

        for perms, signs in rotations:
            rotated = rotate(b_transpose, perms, signs)
            offset = []
            for p in zip(rotated, a_transpose):
                points = set([x[1] - x[0] for x in zip(p[0], p[1])])

                if len(points) == 1:
                    offset.append(points.pop())
                if len(offset) == 3:
                    print(offset, perms, signs)
                    mapping_dict[(i)] = (offset, perms, signs)
                    break
    return mapping_dict, perms, signs


def transform(to_transform, target_center,trans_perm, trans_sign):
    transformed = []
    rotated = rotate(to_transform, trans_perm, trans_sign)
    for i, p in enumerate(rotated):
        transformed.append(list(map(lambda x: target_center[i] + x, p)))
    return transformed


def get_intersections(scanners):
    intersections = []
    for i in permutations(range(len(scanners)), 2):
        a = set(euclid_distance(*p) for p in combinations(scanners[i[0]], 2))
        b = set(euclid_distance(*p) for p in combinations(scanners[i[1]], 2))
        if len(a.intersection(b)) == 66:
            intersections.append(i)
    return intersections


def part_2(scanners):
    pass


def main():
    lines = get_lines("input_19.txt")
    scanners = parse_input(lines)
    print(scanners)
    print("Part 1:", part_1(scanners)) #too low
    print("Part 2:", part_2(scanners))


if __name__ == '__main__':
    main()