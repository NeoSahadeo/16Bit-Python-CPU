Main (main.py)
==============

This page contains how the `main.py` file works.

Instruction Set
***************

The 16-bit processor uses binary instructions
based on a custom instruction list implemented in the :ref:`processor-instruction-module`.


Creating an Instruction Set
------------------------------------------

Let's generate a small set of instructions to see how it works.
The instruction we want to generate:

.. code-block::

  add 3 to 2 -> store in RAM

+-----------------------------------------+---+---+---+---+
| INSTRUCTION SET                         | A | B | C | D |
+=========================================+===+===+===+===+
| Logic or Arithemtic                     | 0 | 1 | 0 | 1 |
+-----------------------------------------+---+---+---+---+
| operation code 1                        | 0 | 0 | 0 | 0 |
+-----------------------------------------+---+---+---+---+
| operation code 2                        | 0 | 0 | 0 | 0 |
+-----------------------------------------+---+---+---+---+
| zero replace                            | 0 | 0 | 0 | 0 |
+-----------------------------------------+---+---+---+---+
| swap                                    | 0 | 0 | 0 | 0 |
+-----------------------------------------+---+---+---+---+
| less than                               | 0 | 0 | 0 | 1 |
+-----------------------------------------+---+---+---+---+
| greater than                            | 0 | 1 | 0 | 0 |
+-----------------------------------------+---+---+---+---+
| equal to                                | 0 | 0 | 0 | 0 |
+-----------------------------------------+---+---+---+---+
| a register                              | 0 | 0 | 0 | 0 |
+-----------------------------------------+---+---+---+---+
| b register                              | 0 | 0 | 0 | 0 |
+-----------------------------------------+---+---+---+---+
| RAM                                     | 0 | 0 | 0 | 0 |
+-----------------------------------------+---+---+---+---+
| select register 'a' or RAM              | 0 | 0 | 0 | 0 |
+-----------------------------------------+---+---+---+---+
|                                         | 0 | 1 | 0 | 0 |
+-----------------------------------------+---+---+---+---+
|                                         | 0 | 0 | 0 | 0 |
+-----------------------------------------+---+---+---+---+
|                                         | 1 | 0 | 1 | 0 |
+-----------------------------------------+---+---+---+---+
| Direct write to register 'a' or use ALU | 1 | 1 | 0 | 1 |  
+-----------------------------------------+---+---+---+---+

Instruction **A** writes the value ``0b11`` (3 in binary) to `register 'a'`

Instruction **B** tells the :ref:`alu` to copy the value in `register 'a'`
to `register 'b'`

Instruction **C** writes the value ``0b10`` (2 in binary) to `register 'a'`

Instruction **D** adds the value in `register 'a'` to the value in `register 'b'`
then write the value in :ref:`ram`

.. NOTE::
   The address of **where** to store the value in RAM is determined by the value
   of `register 'a'`

In Python our instruction becomes

.. code-block::

  instruction_set = [
      0b0000000000000011, # set a_reg = 3
      0b1000001000001001, # set b_reg = a_reg
      0b0000000000000010, # set a_reg = 2
      0b1000010000000001, # set ram(a_reg) = a_reg + b_reg
  ]


Main Process
************

To show that the instructions work I've created a simple computer to
run the instruction set. This involves connecting the :ref:`processor-control-module`,
:ref:`processor-instruction-module`, :ref:`program-counter`, :ref:`unified-memory` and 
:ref:`clock-cycles` together.

The main method in the `Computer` class in `main.py` will follow these steps (based on clock cycles):

1. Load the current instruction into memory
2. Run the calculation process on the bits
3. Write the output into memory
4. Increment the program counter


The rest of the code in the `main.py` file is boilerplate needed
to run the instruction using Python's generator functions.
