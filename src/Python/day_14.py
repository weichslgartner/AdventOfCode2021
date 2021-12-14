from collections import defaultdict
from typing import Dict, List

from aoc import get_lines


def parse_input(lines: List[str]) -> (str, Dict[str, str]):
    return lines[0], {k.strip(): v.strip() for k, v in map(lambda l: l.split('->'), lines[2:])}


def part_1(template: str, insertion_dict: Dict[str, str], rounds: int = 10) -> int:
    return solve(template, insertion_dict, rounds)


def part_2(template: str, insertion_dict: Dict[str, str], rounds: int = 40) -> int:
    return solve(template, insertion_dict, rounds)


def solve(template: str, insertion_dict: Dict[str, str], rounds: int) -> int:
    result_dict = {k: 0 for k in insertion_dict.keys()}
    for i in range(len(template) - 1):
        result_dict[template[i:i + 2]] += 1
    for _ in range(rounds):
        for k, v in list(filter(lambda x: x[1] > 0, result_dict.items())):
            result_dict[k] -= v
            result_dict[k[0] + insertion_dict[k]] += v
            result_dict[insertion_dict[k] + k[1]] += v
    frequency = get_letter_count(template, result_dict)
    return frequency[-1] - frequency[0]


def get_letter_count(template: str, result_dict: Dict[str, int]) -> List[int]:
    letter_count = defaultdict(int)
    for k, v in result_dict.items():
        letter_count[k[0]] += v
        letter_count[k[1]] += v
    letter_count[template[0]] += 1
    letter_count[template[-1]] += 1
    return sorted(v // 2 for v in letter_count.values())


def main():
    lines = get_lines("input_14.txt")
    template, insertion_dict = parse_input(lines)
    print("Part 1:", part_1(template, insertion_dict))
    print("Part 2:", part_2(template, insertion_dict))


if __name__ == '__main__':
    main()
