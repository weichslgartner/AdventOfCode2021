from collections import defaultdict
from pathlib import Path
from typing import Dict, List

START_NODE = "start"
END_NODE = "end"


def parse_input(lines: List[str]) -> Dict[str, List[str]]:
    edges = defaultdict(list)
    for x in map(lambda line: line.split('-'), lines):
        edges[x[0]].append(x[1])
        edges[x[1]].append(x[0])
    return edges


def part_1(edges: Dict[str, List[str]]) -> int:
    return solve(edges, True)


def part_2(edges: Dict[str, List[str]]) -> int:
    return solve(edges, False)


def solve(edges: Dict[str, List[str]], small_twice: bool) -> int:
    n_distinct_paths = 0
    queue = [(v, START_NODE, small_twice) for v in edges[START_NODE]]
    while len(queue) > 0:
        node, path, small_twice = queue.pop()
        path += "," + node
        if node == END_NODE:
            n_distinct_paths += 1
            continue
        for e in edges[node]:
            if e == START_NODE:
                continue
            if e not in path or e.isupper():
                queue.append((e, path, small_twice))
            elif not small_twice:
                queue.append((e, path, True))
    return n_distinct_paths


def main():
    file = Path(__file__).parents[2] / "inputs" / "input_12.txt"
    with file.open('r') as f:
        lines = f.read().splitlines()
    edges = parse_input(lines)
    print("Part 1:", part_1(edges))
    print("Part 2:", part_2(edges))


if __name__ == '__main__':
    main()
