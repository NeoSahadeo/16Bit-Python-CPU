## **Creative Commons Attribution (CC BY)**
## Docs are on the Github repo

from implspec import *
from units import *
from memory import *

class UnifiedMemory:
    """
    bits16 refers to the store value
    """
    def __init__(self):
        self.a_register = Register()
        self.b_register = Register()
        self.ram = RAM()

    def write(self, a, b, ram, bits16, clock):
        self.a_register.write(a, bits16, clock)
        self.b_register.write(b, bits16, clock)
        self.ram.write(ram, self.a_register.read(), bits16, clock)
        return (self.a_register.read(), self.b_register.read(), self.ram.read(bits16))

    def read(self):
        return (self.a_register.read(), self.b_register.read(), self.ram.read(self.a_register.read()))


class Instruction:
    def __init__(self):
        self.unified_memory = UnifiedMemory()
        self.switch = Switch()
        self.alu = ALU()
        self.conditions = Conditions()

    def calc(self, bits16, a_register, b_register, ram):
        """
        bits16 refers to the instruction

        Return type:
            alu value,
            conditional is true,
            a register,
            b register,
            ram
        """

        # Instruction Set:
        # 0 logic or alu
        # 1 op1
        # 2 op2
        # 3 zero replace
        # 4 swap
        # 5 lt
        # 6 gt
        # 7 eq
        # 8 a register
        # 9 b register
        # 10 ram
        # 11 select a-register or ram

        instruction = generate16Bits(bits16)
        select_value = self.switch.select_16(ram, a_register, instruction[11])
        alu_value = self.alu.calc(instruction[0], instruction[1], instruction[2], instruction[3], instruction[4], b_register, select_value)
        is_true = self.conditions.calc(instruction[5], instruction[6], instruction[7], alu_value)

        return (alu_value, is_true, instruction[8], instruction[9], instruction[10])


class ControlUnit:
    def __init__(self):
        self.unified_memory = UnifiedMemory()
        self.switch = Switch()
        self.logic_gates = LogicGates()
        self.instruction = Instruction()

    def calc(self, bits16, a_register, b_register, ram):
        """
        bits16 refers to the instruction

        Return type:
            output value,
            conditional is true,
            a register,
            b register,
            ram
        """
        instruction_bits = generate16Bits(bits16)
        data_or_alu_instr = instruction_bits[15]
        alu_value, conditional, a_register, b_register, ram = self.instruction.calc(bits16, a_register, b_register, ram)

        output = self.switch.select_16(alu_value, bits16, data_or_alu_instr)
        direct_a_write = self.switch.select_16(a_register, 1, data_or_alu_instr)

        and_one = self.logic_gates.and_gate(data_or_alu_instr, b_register)
        and_two = self.logic_gates.and_gate(data_or_alu_instr, ram)
        and_three = self.logic_gates.and_gate(data_or_alu_instr, conditional)

        return (output, and_three, direct_a_write, and_one, and_two)
