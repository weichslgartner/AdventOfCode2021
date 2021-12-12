from collections import defaultdict
from pathlib import Path
from queue import SimpleQueue
from typing import Dict, List


def parse_input(lines: List[str]) -> Dict[str, List[str]]:
    edges_list = [line.split('-') for line in lines]
    edges = defaultdict(list)
    for x in edges_list:
        edges[x[0]].append(x[1])
        edges[x[1]].append(x[0])
    return edges


def part_1(edges:  Dict[str, List[str]]) -> int:
    return solve(edges, True)


def part_2(edges:  Dict[str, List[str]]) -> int:
    return solve(edges, False)


def solve(edges:  Dict[str, List[str]], small_twice: bool) -> int:
    distinct_paths = []
    queue = SimpleQueue()
    for v in edges["start"]:
        queue.put((v, "start", small_twice))
    while not queue.empty():
        node, path, small_twice = queue.get()
        path += "," + node
        if node == "end":
            distinct_paths.append(path)
            continue
        for v in edges[node]:
            if v == "start":
                continue
            if v not in path or v.isupper():
                queue.put((v, path, small_twice))
            elif not small_twice:
                queue.put((v, path, True))
    return len(distinct_paths)


def main():
    file = Path(__file__).parents[2] / "inputs" / "input_12.txt"
    with file.open('r') as f:
        lines = f.read().splitlines()
    edges = parse_input(lines)
    print("Part 1:", part_1(edges))
    print("Part 2:", part_2(edges))


if __name__ == '__main__':
    main()
