from collections import namedtuple
from pathlib import Path

already_won = {}


class Point(namedtuple('Point', 'x y')):
    def __repr__(self):
        return f'{self.y} {self.x}'


def line_to_int(line, split_char=","):
    return [int(i) for i in line.split(split_char) if len(i) > 0]


def parse_input(lines):
    lines.append([])
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


def print_board(hit_board):
    for line in hit_board:
        for c in line:
            print(f" {c} ", end="")
        print("")
    print("")


def has_won(hit_board, p: Point):
    return all(hit_board[p.y]) or all(list(zip(*hit_board))[p.x])


def play_game(draw, boards, boards_hit):
    for cur_num in draw:
        for id_, point2num in boards.items():
            if cur_num in point2num:
                p = point2num[cur_num]
                boards_hit[id_][p.y][p.x] = True
                won = has_won(boards_hit[id_], p)
                score = -1
                if won and id_ not in already_won:
                    score = calc_winning_score(boards_hit, cur_num, id_, point2num)
                yield won, id_, score


def part_1(draw, boards, boards_hit):
    for won, _, score in play_game(draw, boards, boards_hit):
        if won:
            return score


def calc_winning_score(boards_hit, cur_num, id_, point2num):
    point_sum = 0
    for val, point in point2num.items():
        if not boards_hit[id_][point.y][point.x]:
            point_sum += val
    return point_sum * cur_num


def part_2(draw, boards, boards_hit):
    for won, id_, score in play_game(draw, boards, boards_hit):
        if won:
            already_won[id_] = True
            if len(already_won) == len(boards):
                return score


def main():
    file = Path(__file__).parents[2] / "inputs" / "input_04.txt"
    with file.open('r') as f:
        lines = f.read().splitlines()
    draw, boards, boards_hit = parse_input(lines)
    print("Part 1 :", part_1(draw, boards, boards_hit))
    print("Part 2 :", part_2(draw, boards, boards_hit))


if __name__ == '__main__':
    main()
