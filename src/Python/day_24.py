from collections import defaultdict
from enum import Enum

from operator import add, mul, ifloordiv, mod, eq, iadd, imul, imod

from z3 import BitVecVal, If, set_option, Optimize, BitVec

from aoc import get_lines

set_option(max_args=10000000, max_lines=1000000, max_depth=10000000, max_visited=1000000)


class Instr(str, Enum):
    inp = 'inp',
    add = 'add',
    mul = 'mul',
    div = 'div',
    mod = 'mod',
    eql = 'eql',


def zeql(x, y):
    return If(x == y, BitVecVal(1, 64), BitVecVal(0, 64))


operations = {Instr.add: iadd,
              Instr.mul: imul,
              Instr.div: ifloordiv,
              Instr.mod: imod,
              Instr.eql: lambda x, y: int(eq(x, y))
              }


def parse_input(lines):
    blocks = {}
    block = []
    n = 1
    for y, line in enumerate(lines):
        if line.startswith("inp") and len(block) > 0:
            blocks[n] = block
            block = []
            n += 1
        tokens = line.split(' ')
        block.append([Instr(tokens[0]), *[int(t) if t.lstrip('-').isdecimal() else t for t in tokens[1:]]])
    blocks[n] = block
    return blocks


def get_optimizer(blocks):
    opt = Optimize()
    optimize_vars = []
    z_last = 0
    for block_n, block in blocks.items():
        block_variables_index = defaultdict(int)
        z3_variables = {}
        for ins in block:
            if ins[0] == Instr.inp:
                w = BitVec(f"w_{block_n}", 64)
                optimize_vars.append(w)
                opt.add(w > 0)
                opt.add(w < 10)
                z3_variables[f"w_{block_n}"] = w
            else:
                var_left = BitVec(f"{ins[1]}_{block_n}_{block_variables_index[ins[1]]}", 64)

                z3_variables[f"{ins[1]}_{block_n}_{block_variables_index[ins[1]]}"] = var_left
                block_variables_index[ins[1]] += 1
                # first introduction of variable x and y
                if ins[0] == Instr.mul and ins[2] == 0:
                    opt.add(var_left == 0)
                else:
                    if ins[1] == 'z' and block_variables_index[ins[1]] - 2 < 0:
                        var_right = z_last
                    else:
                        var_right = z3_variables[f"{ins[1]}_{block_n}_{block_variables_index[ins[1]] - 2}"]
                    if isinstance(ins[2], int):
                        if ins[0] == Instr.div:
                            opt.add(var_left == var_right / ins[2])
                        elif ins[0] == Instr.mod:
                            opt.add(var_left == var_right % ins[2])
                        elif ins[0] == Instr.add:
                            opt.add(var_left == var_right + ins[2])
                        elif ins[0] == Instr.mul:
                            opt.add(var_left == var_right * ins[2])
                        elif ins[0] == Instr.eql:
                            opt.add(var_left == zeql(var_right, ins[2]))
                        else:
                            print("error")
                    elif ins[2] == 'z':
                        opt.add(var_left == z_last)
                    else:
                        if ins[2] == 'w':
                            var_right2 = z3_variables[f"w_{block_n}"]
                        else:
                            var_right2 = z3_variables[f"{ins[2]}_{block_n}_{block_variables_index[ins[2]] - 1}"]
                        if ins[0] == Instr.add:
                            opt.add(var_left == var_right + var_right2)
                        elif ins[0] == Instr.mul:
                            opt.add(var_left == var_right * var_right2)
                        elif ins[0] == Instr.eql:
                            opt.add(var_left == zeql(var_right, var_right2))
                        else:
                            print("error")
                if ins[1] == 'z':
                    z_last = var_left
    opt.add(z_last == 0)
    return opt, optimize_vars


def part_1(blocks):
    opt, optimize_vars = get_optimizer(blocks)
    optimize_vars = [opt.maximize(w) for w in optimize_vars]
    opt.check()
    return ''.join(str(opti.upper()) for opti in optimize_vars)


def part_2(blocks):
    opt, optimize_vars = get_optimizer(blocks)
    optimize_vars = [opt.minimize(w) for w in optimize_vars]
    opt.check()
    return ''.join(str(opti.lower()) for opti in optimize_vars)


def main():
    lines = get_lines("input_24.txt")
    blocks = parse_input(lines)
    print("Part 1:", part_1(blocks))
    print("Part 2:", part_2(blocks))


if __name__ == '__main__':
    main()
