from functools import reduce

from aoc import get_lines
from enum import Enum


class Field(Enum):
    Version = 1
    Id = 2
    Lateral = 3
    Length_Type_ID = 4
    N_Sub_Packets = 5
    Total_Length_Sub_Packet = 6
    Sub_Packet = 7
    Padding = 8


class Operations(Enum):
    Sum = 0
    Product = 1
    Minimum = 2
    Maximum = 3
    Value = 4
    GT = 5
    LT = 6
    EQ = 7
    OPEN = 8
    CLOSE = 9


class Sub_Packet_Type(Enum):
    Total = 1
    Length = 2
    No_Sub_Packet = 3


bit_lengths = {
    Field.Version: 3,
    Field.Id: 3,
    Field.Lateral: 5,
    Field.Length_Type_ID: 1,
    Field.N_Sub_Packets: 11,
    Field.Total_Length_Sub_Packet: 15,
    Field.Sub_Packet: 11

}


def parse_input(lines):
    return hex_to_bits(lines[0])


def consume_int(bitstream, n_bits):
    return bitstream[n_bits:], int(bitstream[:n_bits], 2)


def consume_raw(bitstream, n_bits):
    return bitstream[n_bits:], bitstream[:n_bits]


def part_1(bitstring):
    parse = Field.Version
    versions = []
    laterals = []
    lateral_raw = ""
    depth = 0
    sub_packet_type = []
    n_sub_packets = {}
    length_subpackets = []
    operation_stack = []
    expressions = []
    while len(bitstring) > 0:
        consumed_bits = 0
        if parse == Field.Version:
            bitstring, version = consume_int(bitstring, bit_lengths[Field.Version])
            consumed_bits = bit_lengths[Field.Version]
            versions.append(version)
            parse_next = Field.Id
        elif parse == Field.Id:
            bitstring, type = consume_int(bitstring, bit_lengths[Field.Id])
            consumed_bits = bit_lengths[Field.Version]
            if type == 4:
                parse_next = Field.Lateral
            else:
                # operator
                print(Operations(type))
                operation_stack.append(Operations(type))
                expressions.append(Operations.OPEN)
                depth += 1
                expressions.append(Operations(type))
                parse_next = Field.Length_Type_ID
        elif parse == Field.Lateral:
            bitstring, not_last = consume_int(bitstring, 1)
            bitstring, lval = consume_raw(bitstring, 4)
            lateral_raw += lval
            consumed_bits = bit_lengths[Field.Lateral]
            if len(length_subpackets) > 0:
                length_subpackets[-1] -= consumed_bits
            if not_last == 0:
                lateral = int(lateral_raw, 2)
                # print(lateral)
                operation_stack.append(lateral)
                expressions.append(lateral)
                if len(length_subpackets) > 0 and length_subpackets[-1] == 0:
                    length_subpackets.pop()
                    expressions.append(Operations.CLOSE)
                    depth -= -1

                lateral_raw = ""
                parse_next = Field.Version
                while depth in n_sub_packets:
                    n_sub_packets[depth] -= 1
                    if n_sub_packets[depth] == 0:
                        del n_sub_packets[depth]
                        expressions.append(Operations.CLOSE)
                        depth -= -1
                    else:
                        break

              #  if len(n_sub_packets) > 0 or len(length_subpackets) > 0:
              #      parse_next = Field.Version
        elif parse == Field.Padding:
            consumed_bits = len(bitstring)
            bitstring, tmp = consume_raw(bitstring, consumed_bits)
        elif parse == Field.Length_Type_ID:
            consumed_bits = bit_lengths[Field.Length_Type_ID]
            bitstring, next = consume_int(bitstring, consumed_bits)
            if next == 1:
                parse_next = Field.N_Sub_Packets
            else:
                parse_next = Field.Total_Length_Sub_Packet
        elif parse == Field.N_Sub_Packets:
            consumed_bits = bit_lengths[Field.N_Sub_Packets]
            bitstring, val = consume_int(bitstring, consumed_bits)
            # print("subpackets", val)
            # if operation_stack[-1] == Operations.GT:
            #     print("asd")
            n_sub_packets[depth] = val
            parse_next = Field.Version
        elif parse == Field.Total_Length_Sub_Packet:
            consumed_bits = bit_lengths[Field.Total_Length_Sub_Packet]
            bitstring, length_subpacket = consume_int(bitstring, consumed_bits)
            print("length packets", length_subpacket)
            if operation_stack[-1] == Operations.GT:
                print("asd")
            length_subpackets.append(length_subpacket)
            parse_next = Field.Version

        if len(length_subpackets) > 0 and parse != Field.Lateral:
            if not parse == Field.Total_Length_Sub_Packet:
                length_subpackets[-1] -= consumed_bits
                if length_subpackets[-1] <= 0:
                    length_subpackets.pop()
            if len(length_subpackets) > 1:
                for i in range(len(length_subpackets) - 1):
                    length_subpackets[i] -= consumed_bits

        parse = parse_next
        print(n_sub_packets)
    # print(versions)
    print(expressions)
    print(operation_stack)
    return sum(versions), expressions


def part_2(operation_stack):
    result = []
    operands = []
    if operation_stack[-1] == Operations.Sum:
        operation_stack.pop()
    if operation_stack[-1] == Operations.OPEN:
        operation_stack.pop()
    n_close = 0
    while len(operation_stack) > 0:
        val = operation_stack.pop()
        if val == Operations.CLOSE:
            n_close += 1
            continue
        if val == Operations.OPEN:
            n_close -= 1
            continue
        if not isinstance(val, Operations) and n_close > 0:
            operands.append(val)
        else:
            print(operands)
            if len(operands) == 0:
                i = 0
                while len(result) > 0 and isinstance(result[-1], int):
                    operands.append(result.pop())
                    i += 1
                    if val in [Operations.EQ, Operations.GT, Operations.LT] and len(operands) == 2:
                        break

            if val == Operations.Sum:
                result.append(sum(operands))

            elif val == Operations.Product:
                result.append(reduce(lambda acc, x: acc * x, operands, 1))
            elif val == Operations.Maximum:
                result.append(max(operands))
            elif val == Operations.Minimum:
                result.append(min(operands))
            elif val == Operations.GT:
                print(len(operands))
                assert len(operands) == 2
                result.append(int(operands[1] > operands[0]))
            elif val == Operations.LT:
                assert len(operands) == 2

                result.append(int(operands[1] < operands[0]))
            elif val == Operations.EQ:
                assert len(operands) == 2

                result.append(int(operands[0] == operands[1]))
            operands = []

    return result[0]


def hex_to_bits(hex_stream):
    return ''.join([f"{int(h, 16):04b}" for h in hex_stream])


def test():
    # _, stack = part_1(hex_to_bits("C200B40A82"))
    # assert part_2(stack) == 3
    # _, stack = part_1(hex_to_bits("04005AC33890"))
    # assert part_2(stack) == 54
    # _, stack = part_1(hex_to_bits("880086C3E88112"))
    # assert part_2(stack) == 7
    # _, stack = part_1(hex_to_bits("CE00C43D881120"))
    # assert part_2(stack) == 9
    # _, stack = part_1(hex_to_bits("D8005AC2A8F0"))
    # assert part_2(stack) == 1
    # _, stack = part_1(hex_to_bits("F600BC2D8F"))
    # assert part_2(stack) == 0
    # _, stack = part_1(hex_to_bits("9C005AC2F8F0"))
    # assert part_2(stack) == 0
    # _, stack = part_1(hex_to_bits("9C0141080250320F1802104A08"))
    # assert part_2(stack) == 1
    # result, _ = part_1(hex_to_bits("8A004A801A8002F478"))
    # assert result == 16
    # result, _ = part_1(hex_to_bits("620080001611562C8802118E34"))
    # assert result == 12
    # result, _ = part_1(hex_to_bits("C0015000016115A2E0802F182340"))
    # assert result == 23
    result, _ = part_1(hex_to_bits("A0016C880162017C3686B18A3D4780"))
    assert result == 31


def main():
    test()
    lines = get_lines("input_16.txt")
    bit_string = parse_input(lines)
    res1, ostack = part_1(bit_string)
    print("Part 1:", res1)
    ostack.pop()
    ostack.pop()
    print(ostack.count(Operations.OPEN))
    print(ostack.count(Operations.CLOSE))

    print("Part 2:", part_2(ostack))


if __name__ == '__main__':
    main()