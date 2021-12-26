from collections import defaultdict
from enum import Enum

import z3

from aoc import get_lines
from operator import add, mul, ifloordiv, mod, eq, iadd, imul, imod
from z3 import Ints, Optimize, Int, Sum, If, set_param, ArithRef, is_idiv, set_option, set_param, Or

set_param('parallel.enable', True)


class Instr(str, Enum):
    inp = 'inp',
    add = 'add',
    mul = 'mul',
    div = 'div',
    mod = 'mod',
    eql = 'eql',


def zeql(x: ArithRef, y: ArithRef):
    return If(x == y, 1, 0)


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


def brute_force(instructions):
    for i in range(int(10e13 - 1), int(1e13), -1):
        p_input = str(i)
        if '0' in p_input:
            continue
        variables = defaultdict(int)
        run_program(instructions, p_input, variables)
        # print(variables['z'])
        if variables['z'] == 0:
            return i





def part_1(blocks):
    set_option(max_args=10000000, max_lines=1000000, max_depth=10000000, max_visited=1000000)
    result = ""
    for i in sorted(blocks.keys(), reverse=True):

        print("position", i)
        if i == 14:
            values, w = get_bounds(blocks, i, [])

        else:
            values, w = get_bounds(blocks, i, values)

        print(values,w)
        result += str(w)
    print(result)
    return result[::-1]


def get_bounds(blocks, i, z_values ):
    opt = Optimize()
    results = []
    optimize_vars = {}
    z_in = Int(f"z_in")
    if i == 1:
        opt.add(z_in == 0)
    else:
        opt.add(z_in > 0)
        opt.add(z_in <  10000)
    z_last = gen_block_constraints(blocks[i], i, opt, optimize_vars, z_in)
    if i == 14:
        opt.add(z_last == 0)
    if i != 1 and len(z_values) > 0:
        clauses =[]
        for val in z_values:
            clauses.append((z_last ==  val))
        opt.add(Or(*clauses))
    print(opt.assertions())
    #print(opt.check())
    u = 0
    while opt.check() == z3.sat and u <35:
        results.append(opt.model()[z_in])
        #print(opt.model())
        opt.add( z_in != opt.model()[z_in])
        u+=1
    print(results)
    return results, optimize_vars[f"w_{i}"].upper()

def gen_block_constraints(block, block_n, opt, optimize_vars, z_in):
    block_variables_index = defaultdict(int)
    z3_variables = {}
    for ins in block:
        if ins[0] == Instr.inp:
            w = Int(f"w_{block_n}")
            optimize_vars[f"w_{block_n}"] =opt.maximize(w)
            opt.add(w > 0)
            opt.add(w < 10)
            z3_variables[f"w_{block_n}"] = w
        else:
            var_left = Int(f"{ins[1]}_{block_n}_{block_variables_index[ins[1]]}")

            z3_variables[f"{ins[1]}_{block_n}_{block_variables_index[ins[1]]}"] = var_left
            block_variables_index[ins[1]] += 1
            # first introduction of variable x and y
            if ins[0] == Instr.mul and ins[2] == 0:
                opt.add(var_left == 0)
            else:
                if ins[1] == 'z' and block_variables_index[ins[1]] - 2 < 0:
                    var_right = z_in
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

                    opt.add(var_left == z_in)
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
    return z_last


def run_program(instructions, p_input, variables):
    # print(p_input)
    # i = 0
    for inst in instructions:
        # print(inst)
        if inst[0] == Instr.inp:
            variables[inst[1]] = int(p_input[0])
            p_input = p_input[1:]
            if variables['z'] > 26:
                return variables
            # print(i,variables)
            # i+=1
        else:
            ops = []
            for t in inst[1:]:
                # print(t, type(t), isinstance(t, str))
                if type(t) == int:
                    ops.append(t)
                else:
                    ops.append(variables[t])
            #  ops = [variables[t] if t is isinstance(t, str) else t for t in inst[1:]]
            # print(inst[0], *ops)
            # if inst[0] == Instr.eql:
            #   print("das")
            res = operations[inst[0]](*ops)
            variables[inst[1]] = res
    return variables


def part_2(lines):
    run_program()


def main():
    lines = get_lines("input_24.txt") # too high 91212119929999
    blocks = parse_input(lines)
    print("Part 1:", part_1(blocks))
#    print("Part 2:", part_2(lines))


if __name__ == '__main__':
    main()
