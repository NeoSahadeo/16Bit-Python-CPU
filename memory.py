from implspec import *
from units import *

class SRLatch:
    def __init__(self):
        self.logic_gates = LogicGates();
        # For testing purposes
        self.nor_one = 0
        self.nor_two = 0

    def data(self, set, reset):
        or_comb_one = self.logic_gates.or_gate(set, self.nor_two)
        self.nor_one = self.logic_gates.invert(or_comb_one)
        or_comb_two = self.logic_gates.or_gate(reset, self.nor_one)
        self.nor_two = self.logic_gates.invert(or_comb_two)
        return self.nor_two


class DataLatch:
    def __init__(self):
        self.logic_gates = LogicGates()
        self.sr_latch = SRLatch()

    def data(self, data, high):
        inv_d = self.logic_gates.invert(data)
        and_comb_one = self.logic_gates.and_gate(data, high)
        and_comb_two = self.logic_gates.and_gate(inv_d, high)
        self.sr_latch.data(and_comb_one, and_comb_two)
        return self.sr_latch.nor_two


class DataFlipFlop:
    def __init__(self):
        self.logic_gates = LogicGates()
        self.data_latch_master = DataLatch()
        self.data_latch_slave = DataLatch()

    def data(self, data, clock):
        inv_clock = self.logic_gates.invert(clock)
        master = self.data_latch_master.data(data, inv_clock)
        inv_clock = self.logic_gates.invert(inv_clock)
        self.data_latch_slave.data(master, inv_clock)
        return self.data_latch_slave.sr_latch.nor_two

class Register:
    def __init__(self):
        self.data_flip_flop_1 = DataFlipFlop()
        self.data_flip_flop_2 = DataFlipFlop()
        self.data_flip_flop_3 = DataFlipFlop()
        self.data_flip_flop_4 = DataFlipFlop()
        self.data_flip_flop_5 = DataFlipFlop()
        self.data_flip_flop_6 = DataFlipFlop()
        self.data_flip_flop_7 = DataFlipFlop()
        self.data_flip_flop_8 = DataFlipFlop()
        self.data_flip_flop_9 = DataFlipFlop()
        self.data_flip_flop_10 = DataFlipFlop()
        self.data_flip_flop_11 = DataFlipFlop()
        self.data_flip_flop_12 = DataFlipFlop()
        self.data_flip_flop_13 = DataFlipFlop()
        self.data_flip_flop_14 = DataFlipFlop()
        self.data_flip_flop_15 = DataFlipFlop()
        self.data_flip_flop_16 = DataFlipFlop()
        # self.value = 0b0

    def write(self, bits16, clock):
        two_bytes = generate16Bits(bits16)
        d1 = self.data_flip_flop_1.data(two_bytes[0], clock) 
        d2 = self.data_flip_flop_2.data(two_bytes[1], clock) 
        d3 = self.data_flip_flop_3.data(two_bytes[2], clock) 
        d4 = self.data_flip_flop_4.data(two_bytes[3], clock) 
        d5 = self.data_flip_flop_5.data(two_bytes[4], clock) 
        d6 = self.data_flip_flop_6.data(two_bytes[5], clock) 
        d7 = self.data_flip_flop_7.data(two_bytes[6], clock) 
        d8 = self.data_flip_flop_8.data(two_bytes[7], clock) 
        d9 = self.data_flip_flop_9.data(two_bytes[8], clock) 
        d10 = self.data_flip_flop_10.data(two_bytes[9], clock)
        d11 = self.data_flip_flop_11.data(two_bytes[10], clock)
        d12 = self.data_flip_flop_12.data(two_bytes[11], clock)
        d13 = self.data_flip_flop_13.data(two_bytes[12], clock)
        d14 = self.data_flip_flop_14.data(two_bytes[13], clock)
        d15 = self.data_flip_flop_15.data(two_bytes[14], clock)
        d16 = self.data_flip_flop_16.data(two_bytes[15], clock)
        return tupleToBinary(((d16,d15,d14,d13,d12,d11,d10,d9,d8,d7,d6,d5,d4,d3,d2,d1)))

    def read(self):
        d1 = self.data_flip_flop_1.data_latch_slave.sr_latch.nor_two
        d2 = self.data_flip_flop_2.data_latch_slave.sr_latch.nor_two
        d3 = self.data_flip_flop_3.data_latch_slave.sr_latch.nor_two
        d4 = self.data_flip_flop_4.data_latch_slave.sr_latch.nor_two
        d5 = self.data_flip_flop_5.data_latch_slave.sr_latch.nor_two
        d6 = self.data_flip_flop_6.data_latch_slave.sr_latch.nor_two
        d7 = self.data_flip_flop_7.data_latch_slave.sr_latch.nor_two
        d8 = self.data_flip_flop_8.data_latch_slave.sr_latch.nor_two
        d9 = self.data_flip_flop_9.data_latch_slave.sr_latch.nor_two
        d10 = self.data_flip_flop_10.data_latch_slave.sr_latch.nor_two
        d11 = self.data_flip_flop_11.data_latch_slave.sr_latch.nor_two
        d12 = self.data_flip_flop_12.data_latch_slave.sr_latch.nor_two
        d13 = self.data_flip_flop_13.data_latch_slave.sr_latch.nor_two
        d14 = self.data_flip_flop_14.data_latch_slave.sr_latch.nor_two
        d15 = self.data_flip_flop_15.data_latch_slave.sr_latch.nor_two
        d16 = self.data_flip_flop_16.data_latch_slave.sr_latch.nor_two
        return tupleToBinary(((d16,d15,d14,d13,d12,d11,d10,d9,d8,d7,d6,d5,d4,d3,d2,d1)))


class Counter:
    def __init__(self):
        self.register = Register()
        self.switch = Switch()
        self.increment_16 = Incremenet16()
        self.logic_gates = LogicGates()
        self.subtract = Subtract16()

    def inc(self, stream, bits16, clock):
        c_value = tupleToBinary(self.increment_16.inc(self.register.read()))
        select_value = self.switch.select_16(bits16, c_value, stream)
        self.register.write(select_value, clock)
        return self.register.read()


class RAM:
    def __init__(self):
        # RAM can be implemented by chaining 
        # registers together and implementing
        # a 4-to-16 (2^4=16) decoder for addressing.
        
        # I thinks its going to be unrealistic
        # to write 64_000 registers that are 
        # hardcoded in Python.
        # The theory remains the same, except I
        # am using arrays to simplify the imple.

        # 2^16 = 65_536
        self.register = [0]*65536

    def read(self, bits16):
        return self.register[bits16]

    def write(self, address, value):
        self.register[address] = value
        return self.register[address]

