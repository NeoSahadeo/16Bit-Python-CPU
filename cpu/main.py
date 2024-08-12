# **MIT LICENSE**

# An emulation of a 16 bit CPU written in Python
## By Neo Sahadeo

import math
from memory import *
from processor import *

# Read only memory
instruction_set = [
    0b0000000000000011, # set a_reg = 3
    0b1000001000001001, # set b_reg = a_reg
    0b0000000000000010, # set a_reg = 2
    0b1000010000000001, # set ram(a_reg) = a_reg + b_reg
]

class Computer:
    def __init__(self):
        # State is runtime based
        self.counter = Counter()
        self.working_memory = UnifiedMemory()
        self.control_unit = ControlUnit()

        # avoid undefined behaviour. Can be fixed by reading from
        # the self.counter function (possibly)
        self.counter_value = 0

    def main_generator(self):
        i = 0
        while True:
            clock = math.ceil(i % 2)
            yield self.main(clock)
            i += 1

    def main(self, clock):
        instruction = instruction_set[self.counter_value]
        output, conditional, a_reg, b_reg, ram = self.control_unit.calc(instruction,
                                   self.working_memory.a_register.read(),
                                   self.working_memory.b_register.read(),
                                   self.working_memory.ram.read(self.working_memory.a_register.read()))
        self.working_memory.a_register.write(a_reg, output, clock)
        self.working_memory.b_register.write(b_reg, output, clock)
        self.working_memory.ram.write(ram, self.working_memory.a_register.read(), output, clock)
        self.counter_value = self.counter.inc(conditional, self.working_memory.a_register.read(), clock)

        # This can be deleted. Just used to see working operations
        if clock == 1:
            print(f"""A reg: {self.working_memory.a_register.read()} 
B reg: {self.working_memory.b_register.read()} 
RAM  : {self.working_memory.ram.read(self.working_memory.a_register.read())}""")
        #### 

if __name__ == '__main__':
    computer = Computer()
    main_gen = computer.main_generator()
    try:
        while True:
            next(main_gen)
    except:
        print('End of Instructions')
