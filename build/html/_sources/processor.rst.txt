Processor (processor.py)
========================

The internal workings of the 16-bit processor.

.. _unified-memory:

Unified Memory 
**************

The 16-bit CPU has three :ref:`storage-locations`; all of which store 16-bit binary
numbers.

- Register A 
- Register B
- Random Access Memory

To learn more about memory: :ref:`memory`

The value in `register 'a'` is used as the memory location for the :ref:`ram`.
`Register 'b'` is used normally.

In the ``UnifiedMemory`` class there are read and write methods.

The **read** method takes no arguments and will return current values:

.. code-block::

   unified_memory.read()
   Output:
     (a_register, b_register, ram_at_a_register)

The **write** method takes in five arguments and will return current values:

.. code-block::

   unified_memory.write(write_to_a, write_to_b, write_to_ram, value_to_write, clock_cycle)
   Output:
     (a_register, b_register, ram_at_value)

It's also possible to directly *read-write* from any of the registers by directly
accessing them and calling the respective *read-write* methods with the respected
arguments.

**An Example of a direct read-write**

.. code-block::

  unified_memory.a_register.write(1, 0b1, clock_cycle)
  unified_memory.b_register.write(1, 0b1, clock_cycle)
  unified_memory.ram.write(1, 0b0, 0b1, clock_cycle)

  unified_memory.a.read()
  unified_memory.b.read()
  unified_memory.ram.read(0b0)

.. _processor-instruction-module:

Instruction Module
******************

A 16-bit number is generated **by-you** which turns off and on bits
that correspond to internal `bindings` to sub-modules in the :ref:`alu`,
:ref:`storage-location`, and :ref:`direct-a-register-write`

:ref:`alu-op-codes` is not required to understand this section but it will help.

+-----------------------------------------+------------+
| INSTRUCTION SET                         |            |
+=========================================+============+
| Logic or Arithemtic                     | ALU SELECT |
+-----------------------------------------+------------+
| operation code 1                        | ARITHMETIC |
+-----------------------------------------+------------+
| operation code 2                        | ARITHMETIC |
+-----------------------------------------+------------+
| zero replace                            | ARITHMETIC |
+-----------------------------------------+------------+
| swap                                    | ARITHMETIC |
+-----------------------------------------+------------+
| less than                               | CONDITIONAL|
+-----------------------------------------+------------+
| greater than                            | CONDITIONAL|
+-----------------------------------------+------------+
| equal to                                | CONDITIONAL|
+-----------------------------------------+------------+
| a register                              | STORE      |
+-----------------------------------------+------------+
| b register                              | STORE      |
+-----------------------------------------+------------+
| RAM                                     | STORE      |
+-----------------------------------------+------------+
| select register 'a' or RAM              | SPECIAL    |
+-----------------------------------------+------------+
|                                         |            |
+-----------------------------------------+------------+
|                                         |            |
+-----------------------------------------+------------+
|                                         |            |
+-----------------------------------------+------------+
| Direct write to register 'a' or use ALU | DIRECT     |
+-----------------------------------------+------------+

The *empty rows* are intentional. Each instruction must be exactly
16-bits long. Each bit corresponds to an action that the :ref:`alu`
must work out (except if bit 16 is 1, in that case it's a direct write
to register 'a').

.. TIP::
   Remember, we read binary backwards when transcribing it horizontally.
   Where the last row in a table it the first bit and vice-verca. In Python,
   we prepend a ``0b`` to the front to indicate that it is a binary number.


Calling the ``calc`` method of the ``Instruction`` class will return the calculated
value based on the arguments supplied and register values.

The `register 'b'` is always read; The `register 'a'` and the `RAM` are swapped
based on the 12th bit.

The arguments supplied are the *instruction*, *register 'a' value*, *register 'b' value*, *ram value*.

.. code-block::

    instruction.calc(instruction, a_register_value, b_register_value, ram_value):

The return value will be the *alu output*, *conditional check*, *register 'a' selected*,
*register 'b' selected* and *ram at register 'a' selected*.

.. code-block::

   (alu_output, conditional_check, write_to_a, write_to_b, write_to_ram)

**Example of using the Instruction Module**

.. code-block::

   instruction.calc(0b1000010000000001,
     unified_memory.a_register.read(),
     unified_memory.b_register.read(),
     unified_memory.ram.read(unified_memory.a_register.read()))

Control Module
**************

The control module functions in much the same way as the instruction module.
The main difference between the ability to use a **data instruction** (which
is a fancy way to say `write this number to register 'a'`)

All the arguments and return values are identical except the *16th* bit in 
the instruction operates to switch between a **data instruction** and an
**alu instruction** (0 and 1 respectively).
