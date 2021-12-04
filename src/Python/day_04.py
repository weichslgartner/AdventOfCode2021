from collections import namedtuple
from functools import reduce
from pathlib import Path
from typing import List, Dict


class Point(namedtuple('Point', 'x y')):
    def __repr__(self):
        return f'{self.y} {self.x}'


def line_to_int(line: str, split_char=",") -> List[int]:
    return [int(i) for i in line.split(split_char) if len(i) > 0]


def parse_input(lines: List[str]) -> (List[int], Dict, Dict):
    lines.append("")
    draw = line_to_int(lines[0], split_char=",")
    point2num = {}
    hit_board = []
    id_ = 0
    boards = {}
    boards_hit = {}
    y = 0
    for line in lines[2:]:
        if len(line) == 0:
            boards[id_] = point2num
            boards_hit[id_] = hit_board
            id_ += 1
            y = 0
            point2num = {}
            hit_board = []
        else:
            cur_line = line_to_int(line, split_char=" ")
            hit_board.append([False for _ in range(len(cur_line))])
            for x, num in enumerate(cur_line):
                point2num[num] = Point(x, y)
            y += 1
    return draw, boards, boards_hit


def has_won(hit_board: Dict, p: Point) -> bool:
    return all(hit_board[p.y]) or all(list(zip(*hit_board))[p.x])


def play_game(draw: List[int], boards: Dict, boards_hit: Dict, already_won: Dict[int, bool]) -> (bool, int, int):
    score = -1
    for cur_num in draw:
        for id_, point2num in boards.items():
            # if already won, don't care
            if id_ in already_won:
                yield True, id_, score
            if cur_num in point2num:
                p = point2num[cur_num]
                boards_hit[id_][p.y][p.x] = True
                won = has_won(boards_hit[id_], p)
                if won:
                    score = calc_winning_score(boards_hit, cur_num, id_, point2num)
                yield won, id_, score


def calc_winning_score(boards_hit: Dict, cur_num: int, id_: int, point2num: Dict) -> int:
    return reduce(lambda s, p: s + p[0] if not boards_hit[id_][p[1].y][p[1].x] else s, point2num.items(), 0) * cur_num


def part_1(draw: List[int], boards: Dict, boards_hit: Dict, already_won: Dict[int, bool]) -> int:
    for won, _, score in play_game(draw, boards, boards_hit, already_won):
        if won:
            return score


def part_2(draw: List[int], boards: Dict, boards_hit: Dict, already_won: Dict[int, bool]) -> int:
    for won, id_, score in play_game(draw, boards, boards_hit, already_won):
        if won:
            already_won[id_] = True
            if len(already_won) == len(boards):
                return score


def main():
    file = Path(__file__).parents[2] / "inputs" / "input_04.txt"
    with file.open('r') as f:
        lines = f.read().splitlines()
    draw_nums, boards, boards_hit = parse_input(lines)
    already_won = {}
    print("Part 1 :", part_1(draw_nums, boards, boards_hit, already_won))
    print("Part 2 :", part_2(draw_nums, boards, boards_hit, already_won))


if __name__ == '__main__':
    main()
