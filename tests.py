import unittest
from main import *

# You will see 65535, that is the integer limit
# for a 16 bit binary number
# 65535 is x=[(2^16)-1] (all bits are 1)

class TestGates(unittest.TestCase):
    def setUp(self):
        self.logic_gates = LogicGates()
        self.logic_gates_16 = LogicGates16()

    def test_nand_gate(self):
        self.assertEqual(self.logic_gates.nand_gate(0, 0), 1)
        self.assertEqual(self.logic_gates.nand_gate(0, 1), 1)
        self.assertEqual(self.logic_gates.nand_gate(1, 0), 1)
        self.assertEqual(self.logic_gates.nand_gate(1, 1), 0)

    def test_invert(self):
        self.assertEqual(self.logic_gates.invert(1), 0)
        self.assertEqual(self.logic_gates.invert(0), 1)

    def test_and_gate(self):
        self.assertEqual(self.logic_gates.and_gate(0, 0), 0)
        self.assertEqual(self.logic_gates.and_gate(0, 1), 0)
        self.assertEqual(self.logic_gates.and_gate(1, 0), 0)
        self.assertEqual(self.logic_gates.and_gate(1, 1), 1)

    def test_or_gate(self):
        self.assertEqual(self.logic_gates.or_gate(0, 0), 0)
        self.assertEqual(self.logic_gates.or_gate(0, 1), 1)
        self.assertEqual(self.logic_gates.or_gate(1, 0), 1)
        self.assertEqual(self.logic_gates.or_gate(1, 1), 1)

    def test_xor_gate(self):
        self.assertEqual(self.logic_gates.xor_gate(0, 0), 0)
        self.assertEqual(self.logic_gates.xor_gate(1, 0), 1)
        self.assertEqual(self.logic_gates.xor_gate(0, 1), 1)
        self.assertEqual(self.logic_gates.xor_gate(1, 1), 0)

    def test_nand_gate_16(self):
        self.assertEqual(self.logic_gates_16.nand_gate(0b0, 0b0), 65535)
        self.assertEqual(self.logic_gates_16.nand_gate(0b0, 0b1), 65535)
        self.assertEqual(self.logic_gates_16.nand_gate(0b1, 0b0), 65535)
        self.assertEqual(self.logic_gates_16.nand_gate(0b1, 0b1), 65534)
        self.assertEqual(self.logic_gates_16.nand_gate(0b10, 0b10), 65533)
        self.assertEqual(self.logic_gates_16.nand_gate(0b1, 0b0001), 65534)

    def test_and_gate_16(self):
        self.assertEqual(self.logic_gates_16.and_gate(0b0, 0b0), 0)
        self.assertEqual(self.logic_gates_16.and_gate(0b0, 0b1), 0)
        self.assertEqual(self.logic_gates_16.and_gate(0b1, 0b0), 0)
        self.assertEqual(self.logic_gates_16.and_gate(0b1, 0b1), 1)
        self.assertEqual(self.logic_gates_16.and_gate(0b01, 0b01), 1)
        self.assertEqual(self.logic_gates_16.and_gate(0b10, 0b10), 2)

    def test_invert_16(self):
        self.assertEqual(self.logic_gates_16.invert(0b1), 65534)
        self.assertEqual(self.logic_gates_16.invert(0b10), 65533)
        self.assertEqual(self.logic_gates_16.invert(0), 65535)
        self.assertEqual(self.logic_gates_16.invert(0b1111111111111111), 0)

    def test_or_16(self):
        self.assertEqual(self.logic_gates_16.or_gate(0b0, 0b0), 0)
        self.assertEqual(self.logic_gates_16.or_gate(0b0, 0b1), 1)
        self.assertEqual(self.logic_gates_16.or_gate(0b1, 0b0), 1)
        self.assertEqual(self.logic_gates_16.or_gate(0b1, 0b1), 1)
        self.assertEqual(self.logic_gates_16.or_gate(0b10, 0b00), 2)
        self.assertEqual(self.logic_gates_16.or_gate(0b00, 0b10), 2)

    def a_test_xor_16(self):
        self.assertEqual(self.logic_gates.xor_gate(0b0, 0b0), 0)
        self.assertEqual(self.logic_gates.xor_gate(0b1, 0b0), 1)
        self.assertEqual(self.logic_gates.xor_gate(0b0, 0b1), 1)
        self.assertEqual(self.logic_gates.xor_gate(0b1, 0b1), 0)
        self.assertEqual(self.logic_gates.xor_gate(0b10, 0b10), 0)

class TestAdders(unittest.TestCase):
    def setUp(self):
        self.half_adder = HalfAdder()
        self.full_adder = FullAdder()
        # multibit adder skipped
        self.bit_adder_16 = BitAdder16()
        self.increment_16 = Incremenet16()
        self.subtract_16 = Subtract16()

    def test_half_adder(self):
        self.assertEqual(self.half_adder.add(1, 1), (1, 0))
        self.assertEqual(self.half_adder.add(0, 1), (0, 1))
        self.assertEqual(self.half_adder.add(1, 0), (0, 1))
        self.assertEqual(self.half_adder.add(0, 0), (0, 0))

    def test_full_adder(self):
        self.assertEqual(self.full_adder.add(1, 1, 1), (1, 1))
        self.assertEqual(self.full_adder.add(1, 0, 1), (1, 0))
        self.assertEqual(self.full_adder.add(0, 1, 0), (0, 1))
        self.assertEqual(self.full_adder.add(1, 0, 0), (0, 1))

    def test_bit_adder_16(self):
        self.assertEqual(self.bit_adder_16.add(0b1, 0b1, 0), (0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0)) # 1+1
        self.assertEqual(self.bit_adder_16.add(0b101, 0b10, 0), (0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1)) # 5+2
        self.assertEqual(self.bit_adder_16.add(0b0, 0b11, 1), (0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0)) # 3+1(c)

    def test_increment_16(self):
        self.assertEqual(self.increment_16.inc_by_1(0b0), (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1))
        self.assertEqual(self.increment_16.inc_by_1(0b1), (0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0))
        self.assertEqual(self.increment_16.inc_by_1(0b10), (0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1))
        self.assertEqual(self.increment_16.inc_by_1(), (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1))

    def test_subtract_16(self):
        self.assertEqual(self.subtract_16.sub(0b1, 0b1), (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)) # 1-1
        self.assertEqual(self.subtract_16.sub(0b0, 0b1), (1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1)) # 0-1
        self.assertEqual(self.subtract_16.sub(0b11, 0b10), (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1)) # 3-2


class TestSwitches(unittest.TestCase):
    def setUp(self):
        self.switch = Switch()

    def test_select(self):
        self.assertEqual(self.switch.select(0, 1, 1), 0)
        self.assertEqual(self.switch.select(0, 1, 0), 1)

    def test_select_16(self):
        self.assertEqual(self.switch.select_16(0b11, 0b10, 0), 2)
        self.assertEqual(self.switch.select_16(0b11, 0b10, 1), 3)

    def test_switch(self):
        self.assertEqual(self.switch.switch(1, 0), (0, 1))
        self.assertEqual(self.switch.switch(1, 1), (1, 0))

class TestALU(unittest.TestCase):
    def setUp(self):
        self.logic_unit = LogicUnit()
        self.arithmetic_unit = ArithmeticUnit()
        self.alu = ALU()
    
    def test_logic_unit(self):
        self.assertEqual(self.logic_unit.calc(0, 0, 0b100, 0b11), 0)
        self.assertEqual(self.logic_unit.calc(1, 0, 0b100, 0b11), 7)
        self.assertEqual(self.logic_unit.calc(0, 1, 0b100, 0b11), 7)
        self.assertEqual(self.logic_unit.calc(1, 1, 0b100, 0b11), 65531)

    def test_arithmetic_unit(self):
        self.assertEqual(self.arithmetic_unit.calc(0, 0, 0b101, 0b100), 9)
        self.assertEqual(self.arithmetic_unit.calc(1, 0, 0b101, 0b100), 1)
        self.assertEqual(self.arithmetic_unit.calc(0, 1, 0b101, 0b100), 6)
        self.assertEqual(self.arithmetic_unit.calc(1, 1, 0b101, 0b100), 4)

    def test_alu_whole(self):
        self.assertEqual(self.alu.calc(1, 1, 0, 0, 0, 0b11, 0b1), 2)
        self.assertEqual(self.alu.calc(1, 0, 0, 0, 0, 0b11, 0b1), 4)
        self.assertEqual(self.alu.calc(0, 1, 0, 0, 0, 0b11, 0b1), 2)
        self.assertEqual(self.alu.calc(1, 1, 1, 0, 0, 0b11, 0b1), 2)
        self.assertEqual(self.alu.calc(0, 1, 1, 0, 0, 0b11, 0b1), 65532)
        self.assertEqual(self.alu.calc(0, 1, 1, 0, 0, 0b0, 0b0), 65535)
        self.assertEqual(self.alu.calc(1, 1, 0, 0, 1, 0b101, 0b10), 65533)
        self.assertEqual(self.alu.calc(1, 1, 0, 0, 0, 0b101, 0b10), 3)
        self.assertEqual(self.alu.calc(1, 1, 0, 1, 0, 0b101, 0b10), 65534)
        self.assertEqual(self.alu.calc(1, 1, 0, 1, 1, 0b101, 0b10), 65531)


# The functions exist due to implementations in Python
# and to make my life slightly more abstracted.
# It's not needed otherwise
class TestGeneration(unittest.TestCase):
    def test_generate16(self):
        self.assertEqual(generate16Bits(0b0), tuple([0]*16))
        self.assertEqual(generate16Bits(0b10), (0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0))

    def test_generateStream(self):
        self.assertEqual(generateStreamBits(1), 65535)
        self.assertEqual(generateStreamBits(0), 0)

class TestMisc(unittest.TestCase):
    def test_tuple_to_binary(self):
        self.assertEqual(tupleToBinary((0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0)), 2)
        self.assertEqual(tupleToBinary((0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1)), 9)

    def test_decimal_to_binary(self):
        self.assertEqual(decimalToBinary(2), 2)


if __name__ == '__main__':
    unittest.main()
