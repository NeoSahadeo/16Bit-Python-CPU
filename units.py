from implspec import *

class LogicGates:
    # These are the base gates
    # The logic gates are built with Python operations
    # and are all extended from NAND
    def nand_gate(self, a, b):
        # This is the simplest I wanted to make it.
        bit = -1 * (int(a & b) - 1)
        return bit

    def invert(self, a):
        bit = self.nand_gate(a, a)
        return bit

    def and_gate(self, a, b):
        bit = self.nand_gate(a, b)
        inv_bit = self.invert(bit)
        return inv_bit

    def or_gate(self, a, b):
        inv_a = self.invert(a)
        inv_b = self.invert(b)
        bit = self.nand_gate(inv_a, inv_b)
        return bit

    def xor_gate(self, a, b):
        nand_comb = self.nand_gate(a, b)
        nand_comb_a = self.nand_gate(nand_comb, a)
        nand_comb_b = self.nand_gate(nand_comb, b)
        bit = self.nand_gate(nand_comb_a, nand_comb_b)
        return bit

class LogicGates16:
    def __init__(self):
        self.logic_gates = LogicGates()

    def nand_gate(self, bits16_one, bits16_two):
        bytes_one = generate16Bits(bits16_one)
        bytes_two = generate16Bits(bits16_two)
        g1 = self.logic_gates.nand_gate(bytes_one[0], bytes_two[0])
        g2 = self.logic_gates.nand_gate(bytes_one[1], bytes_two[1])
        g3 = self.logic_gates.nand_gate(bytes_one[2], bytes_two[2])
        g4 = self.logic_gates.nand_gate(bytes_one[3], bytes_two[3])
        g5 = self.logic_gates.nand_gate(bytes_one[4], bytes_two[4])
        g6 = self.logic_gates.nand_gate(bytes_one[5], bytes_two[5])
        g7 = self.logic_gates.nand_gate(bytes_one[6], bytes_two[6])
        g8 = self.logic_gates.nand_gate(bytes_one[7], bytes_two[7])
        g9 = self.logic_gates.nand_gate(bytes_one[8], bytes_two[8])
        g10 = self.logic_gates.nand_gate(bytes_one[9], bytes_two[9])
        g11 = self.logic_gates.nand_gate(bytes_one[10], bytes_two[10])
        g12 = self.logic_gates.nand_gate(bytes_one[11], bytes_two[11])
        g13 = self.logic_gates.nand_gate(bytes_one[12], bytes_two[12])
        g14 = self.logic_gates.nand_gate(bytes_one[13], bytes_two[13])
        g15 = self.logic_gates.nand_gate(bytes_one[14], bytes_two[14])
        g16 = self.logic_gates.nand_gate(bytes_one[15], bytes_two[15])
        return tupleToBinary((g16,g15,g14,g13,g12,g11,g10,g9,g8,g7,g6,g5,g4,g3,g2,g1))

    def and_gate(self, bits16_one, bits16_two):
        inv_nand = self.nand_gate(bits16_one, bits16_two)
        and_gate = self.invert(inv_nand)
        return and_gate

    def or_gate(self, bits16_one, bits16_two):
        inv_one = self.invert(bits16_one)
        inv_two = self.invert(bits16_two)
        or_gate = self.nand_gate(inv_one, inv_two)
        return or_gate

    def xor_gate(self, bits16_one, bits16_two):
        nand_comb = self.nand_gate(bits16_one, bits16_two)
        nand_comb_a = self.nand_gate(nand_comb, bits16_one)
        nand_comb_b = self.nand_gate(nand_comb, bits16_two)
        xor_gate = self.nand_gate(nand_comb_a, nand_comb_b)
        return xor_gate

    def invert(self, bits16):
        inv = self.nand_gate(bits16, bits16)
        return inv

class HalfAdder:
    def __init__(self):
        self.logic_gates = LogicGates()

    # Half-adders add two bits together.
    def add(self, a, b):
        nand_comb = self.logic_gates.nand_gate(a, b)
        nand_comb_a = self.logic_gates.nand_gate(nand_comb, a)
        nand_comb_b = self.logic_gates.nand_gate(nand_comb, b)
        low_bit = self.logic_gates.nand_gate(nand_comb_a, nand_comb_b)
        high_bit = self.logic_gates.invert(nand_comb)
        return (high_bit, low_bit)

class FullAdder:
    # A full-adder is two half-adders glued together
    # It provides overflow "carry" bits
    def __init__(self):
        self.logic_gates = LogicGates()
        self.half_adder = HalfAdder()

    def add(self, a, b, carry):
        high_one, low_one = self.half_adder.add(a, b)
        high_two, low_two = self.half_adder.add(low_one, carry)
        high_bit = self.logic_gates.or_gate(high_two, high_one)
        low_bit = low_two
        return (high_bit, low_bit)

class MultbitAdder:
    # The multibit adder is how the fundementals of 16bit
    # adder works
    def __init__(self):
        self.full_adder= FullAdder()

    def add(self, a1, a2, b1, b2, carry):
        high_one, low_one = self.full_adder(a2, b2, carry)
        high_two, low_two = self.full_adder(a1, b1, high_one)
        carry = high_two
        return (carry, low_two, low_one)

class BitAdder16:
    # Adds two 16bit binary numbers
    def __init__(self):
        self.full_adder = FullAdder()

    def add(self, bits16_one, bits16_two, carry):
        byte_one = generate16Bits(bits16_one)
        byte_two = generate16Bits(bits16_two)

        h1, l1 = self.full_adder.add(byte_one[0], byte_two[0], carry)
        h2, l2 = self.full_adder.add(byte_one[1], byte_two[1], h1)
        h3, l3 = self.full_adder.add(byte_one[2], byte_two[2], h2)
        h4, l4 = self.full_adder.add(byte_one[3], byte_two[3], h3)
        h5, l5 = self.full_adder.add(byte_one[4], byte_two[4], h4)
        h6, l6 = self.full_adder.add(byte_one[5], byte_two[5], h5)
        h7, l7 = self.full_adder.add(byte_one[6], byte_two[6], h6)
        h8, l8 = self.full_adder.add(byte_one[7], byte_two[7], h7)
        h9, l9 = self.full_adder.add(byte_one[8], byte_two[8], h8)
        h10, l10 = self.full_adder.add(byte_one[9], byte_two[9], h9)
        h11, l11 = self.full_adder.add(byte_one[10], byte_two[10], h10)
        h12, l12 = self.full_adder.add(byte_one[11], byte_two[11], h11)
        h13, l13 = self.full_adder.add(byte_one[12], byte_two[12], h12)
        h14, l14 = self.full_adder.add(byte_one[13], byte_two[13], h13)
        h15, l15 = self.full_adder.add(byte_one[14], byte_two[14], h14)
        h16, l16 = self.full_adder.add(byte_one[15], byte_two[15], h15)
        high_bit = h16
        return (l16,l15,l14,l13,l12,l11,l10,l9,l8,l7,l6,l5,l4,l3,l2,l1)

class Incremenet16:
    def __init__(self):
        self.bit_adder_16 = BitAdder16()
    def inc(self, bits16 = 0b0):
        inc_value = self.bit_adder_16.add(bits16, 0b0, 1)
        return inc_value

class Subtract16:
    def __init__(self):
        self.logic_gates_16 = LogicGates16()
        self.bit_adder_16 = BitAdder16()
        self.increment_16 = Incremenet16()
    def sub(self, bits16_one, bits16_two):
        inv_two = self.logic_gates_16.invert(bits16_two)
        # sub_value = self.bit_adder_16.add(bits16_one, inv_two, 1)[1:]# dicard carry bit
        sub_value = self.bit_adder_16.add(bits16_one, inv_two, 1)
        return sub_value

class Switch:
    # Switch has two methods to switch 
    # outputs of data and data streams
    def __init__(self):
        self.logic_gates = LogicGates()
        self.logic_gates_16 = LogicGates16()

    def select(self, d1, d2, stream):
        inv_stream = self.logic_gates.invert(stream)
        and_gate_one = self.logic_gates.and_gate(inv_stream, d2)
        and_gate_two = self.logic_gates.and_gate(stream, d1)
        stream_out = self.logic_gates.or_gate(and_gate_one, and_gate_two)
        return stream_out

    def switch(self, d, stream):
        inv_stream = self.logic_gates.invert(stream)
        stream_out_one =  self.logic_gates.and_gate(stream, d)
        stream_out_two = self.logic_gates.and_gate(inv_stream, d)
        return (stream_out_one, stream_out_two)

    def select_16(self, d1_16bits, d2_16bits, stream):
        stream_bits = generateStreamBits(stream)
        inv_stream_bits = self.logic_gates_16.invert(stream_bits)
        and_gate_one = self.logic_gates_16.and_gate(inv_stream_bits, d2_16bits)
        and_gate_two = self.logic_gates_16.and_gate(stream_bits, d1_16bits)
        stream_out = self.logic_gates_16.or_gate(and_gate_one, and_gate_two)
        return stream_out

class LogicUnit:
    def __init__(self):
        self.logic_gates_16 = LogicGates16()
        self.switch = Switch()

    def calc(self, op1, op2,  bits16_one, bits16_two):

        inv_one = self.logic_gates_16.invert(bits16_one)
        xor_comb = self.logic_gates_16.xor_gate(bits16_one, bits16_two)
        or_comb = self.logic_gates_16.or_gate(bits16_one, bits16_two)
        and_comb = self.logic_gates_16.and_gate(bits16_one, bits16_two)

        select_one = self.switch.select_16(inv_one, xor_comb, op2)
        select_two = self.switch.select_16(or_comb, and_comb, op2)
        stream_out = self.switch.select_16(select_one, select_two, op1)
        return stream_out

class ArithmeticUnit:
    def __init__(self):
        self.switch = Switch()
        self.bit_adder_16 = BitAdder16()
        self.subtract_16 = Subtract16()

    def calc(self, op1, op2,  bits16_one, bits16_two):
        select_one = self.switch.select_16(1, bits16_two, op2)
        add_value = tupleToBinary(self.bit_adder_16.add(bits16_one, select_one, 0))
        sub_value = tupleToBinary(self.subtract_16.sub(bits16_one, select_one))
        stream_out = self.switch.select_16(sub_value, add_value, op1)
        return stream_out


class ALU:
    def __init__(self):
        self.logic_unit = LogicUnit()
        self.arithmetic_unit = ArithmeticUnit()
        self.switch = Switch()

    def calc(self, logic_or_arith, op1, op2, zero_replace, swap, bits16_one, bits16_two):
        select_one = self.switch.select_16(bits16_two, bits16_one, swap)
        select_two = self.switch.select_16(bits16_one, bits16_two, swap)
        select_three = self.switch.select_16(0, select_one, zero_replace)

        arith = self.arithmetic_unit.calc(op1, op2, select_three, select_two)
        logic = self.logic_unit.calc(op1, op2, select_three, select_two)
        stream_out = self.switch.select_16(arith, logic, logic_or_arith)
        return stream_out


class Conditions:
    def __init__(self):
        self.logic_gates = LogicGates()
        self.logic_gates_16 = LogicGates16()

    def is_zero_2(self, a, b):
        or_comb = self.logic_gates.or_gate(a, b)
        is_zero = self.logic_gates.invert(or_comb)
        return is_zero

    def is_zero_4(self, bits4):
        nibble = generate4Bits(bits4)
        is_zero_one = self.is_zero_2(nibble[0], nibble[1])
        is_zero_two = self.is_zero_2(nibble[2], nibble[3])
        is_zero = self.logic_gates.and_gate(is_zero_one, is_zero_two)
        return is_zero

    def is_zero_8(self, bits8):
        byte = generate8Bits(bits8)
        is_zero_one = self.is_zero_4(tupleToBinary((byte[0], byte[1], byte[2], byte[3])))
        is_zero_two = self.is_zero_4(tupleToBinary((byte[4], byte[5], byte[6], byte[7])))
        is_zero = self.logic_gates.and_gate(is_zero_one, is_zero_two)
        return is_zero

    def is_zero_16(self, bits16):
        two_bytes = generate16Bits(bits16)
        is_zero_one = self.is_zero_8(tupleToBinary((two_bytes[0], two_bytes[1], two_bytes[2], two_bytes[3], two_bytes[4], two_bytes[5], two_bytes[6], two_bytes[7])))
        is_zero_two = self.is_zero_8(tupleToBinary((two_bytes[8], two_bytes[9], two_bytes[10], two_bytes[11], two_bytes[12], two_bytes[13], two_bytes[14], two_bytes[15])))
        is_zero = self.logic_gates.and_gate(is_zero_one, is_zero_two)
        return is_zero

    def calc(self, lt, gt, eq, bits16):
        two_bytes = reverseBits(generate16Bits(bits16))
        neg = isLessThanZero(two_bytes)
        is_zero = self.is_zero_16(bits16)

        nand_comb_one = self.logic_gates.nand_gate(neg, lt)
        nand_comb_two = self.logic_gates.nand_gate(is_zero, eq)
        or_comb = self.logic_gates.or_gate(neg, is_zero)
        inv_or_comb = self.logic_gates.invert(or_comb)

        nand_comb_three = self.logic_gates.nand_gate(inv_or_comb, gt)
        and_comb = self.logic_gates.and_gate(nand_comb_one, nand_comb_two)
        output = self.logic_gates.nand_gate(nand_comb_three, and_comb)

        return output
