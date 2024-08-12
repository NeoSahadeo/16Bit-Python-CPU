Memory (memory.py)
==================

This explains how memory works in the 16-bit CPU. To understand information on this page requires a basic understanding of 
truth tables and logic gates

.. _memory:

What is 'memory'
****************

  Memory is defined loosley as the ability to recall information that is stored somewhere.

Computers can't remember anything that isn't hard-coded in hardware. Solid State Drives 
use mosfets that contruct NAND or NOR gates. Hard Disk Drives use magnetic disks with a
read/write header to store data. These storage methods are *non-volatile*

Volatile and Non-volatile
-------------------------

Volatility of memory decribes whether constant electrical flow is required to maintain
memory. **RAM** as you may have heard is a volatile memory type. It only exists while
the computer is running. As you'll read in :ref:`processor-instruction-module` RAM
can only be addressed using the `register 'a'`.

RAM looses charge over time which
requires it to be constantly refreshed. This refresh rate gives way to SRAM and DRAM.
When the power supply it stopped the refresh of the cells stop and the memory is lost;
hence volatility.

On the other side of this we have memory that is maintained when electrical flow is stopped.
The downside of this method of storage is slower access times and a limited number of read
and writes.

For the 16-bit CPU, volatile memory is the only way to effectively keep-up with the processing
speed of the CPU as well as write the base programs to interact with other storage hardware
in the first place.

Set-Reset Latch
***************

+-----+-------+-----------+
| SET | RESET | OUTPUT    |
+=====+=======+===========+
| 0   | 0     | PREVIOUS  |
+-----+-------+-----------+
| 0   | 1     | 0         |
+-----+-------+-----------+
| 1   | 0     | 1         |
+-----+-------+-----------+
| 1   | 1     | UNDEFINED |
+-----+-------+-----------+

When reset is 1 we want the output to be 0.
When set is 1 we want the output to be 1.
If both set and reset are 0 we want the value that is currently stored.
Undefined behaviour means that it's not specified in the documentation and should not be used **EVER**.

Using the data method from the ``SRLatch`` class directly:

Arguments needed are a `set` and `reset` value.

The return value is the `high-bit`.

.. code-block::

   sr_latch.data(0, 1)
   Output: 0

   sr_latch.data(1, 0)
   Output: 1

   sr_latch.data(0, 0)
   Output: 1


Data Latch
**********

We need to fix make sure that we don't get undefined behaviour when both set and reset are 1.
A data latch is a little bit of logic added on top of an SR-Latch to stop both values
from being equal to eachother.

This is achieved by adding a `data` and `enable` bit. The inversion of the `data` bit with
the same `enable` bit ensures that we cannot produce a ``1 1`` output for the SR-Latch.

+--------+------+--------+--------+
| ENABLE | DATA | OUTPUT | MEMORY |
+========+======+========+========+
|  1     | 0    | 0      | RESET  |
+--------+------+--------+--------+
|  1     | 1    | 1      |  SET   |
+--------+------+--------+--------+


Using the data method from the ``DataLatch`` class directly:

Arguments needed are a `data` and `high` value.

The return value is the `high-bit`.

.. code-block::

   data_latch.data(0, 1)
   Output: 0

   data_latch.data(1, 1)
   Output: 1

   data_latch.data(0, 0)
   Output: 1

Data Flip-Flop
********************

The next priority is fixing race conditions. Currently running Data Lacthes in parallel
will result in some latches changing values before others. The is random behaviour and it's
outcome is undefined.

In order to fix this we need to sync bit updates with a :ref:`clock-cycle`.

Implementing such a cycle is relatively straightforward and can be achieved by chaining
two data latches together (*master* and *slave* respectively).


+------+-------+--------+-----------+
| DATA | CLOCK | OUTPUT | MEMORY    |
+======+=======+========+===========+
| 0    | 0     | 0      | NO CHANGE |
+------+-------+--------+-----------+
| 0    | 1     | 0      | RESET     |
+------+-------+--------+-----------+
| 1    | 0     | 0      | NO CHANGE |
+------+-------+--------+-----------+
| 1    | 1     | 1      | SET       |
+------+-------+--------+-----------+

An new value is introduced in the data flip-flop; **store** bit. This
allows the option to choose whether or not to store the value if a value
is present. This is useful when switch between different registers but only
wanting to modifiy a specific register.

Using the data method from the ``DataFlipFlop`` class directly:

Arguments needed are a `store`, `data` and `clock` value.

The return value is the `high-bit`.

.. code-block::

   data_flip_flop.data(1, 0, 0)
   data_flip_flop.data(1, 0, 1)
   Output: 0

   data_flip_flop.data(1, 1, 0)
   data_flip_flop.data(1, 1, 1)
   Output: 1

   data_flip_flop.data(0, 0, 0)
   data_flip_flop.data(0, 0, 1)
   Output: 0

The method needs to be called twice. Once with the value wanted to be stored
when the clock is on low and another to store the value when the clock is high.

Registers
*********

A register is a group of data flip-flops. Since this is a 16-bit CPU, the register
will have 16 data flip-flops.

The **read** method requires no arguments and returns the currently stored value
in the register.

Using the **write** method from the ``Register`` class directly:
I've implemented a Python specific function that generates a 16-bit number given any
binary number less than 17 (n < 17); This makes programming tests easier.

Arguments needed are a `store`, `bits` and `clock` value.

The return value is the `16_bit_binary`.

.. code-block::

        register.write(1, 0b01, 0)
        register.write(1, 0b1, 1)
        register.read()
        Output: 1

        register.write(1, 0b10, 0)
        register.write(1, 0b10, 1)
        register.read()
        Output: 2

.. _ram:

Random Access Memory
********************

The method the RAM uses to store values boil down to set-reset latches.

In order to implement a **randomly** accessible memory the circuitry needs
a way to tell the difference between bits that have different binary values
but still have the same number of bits on. 

For example, how would a circuit
tell the difference between ``0b100`` (4 in binary) and ``0b10`` (2 in binary).
Both of them have the same number of '1' bits and it gets arbitrarily difficult 
as the number of bits increases.

A circuit known as a **decoder** is needed to assign a unique address to each bit
in a 16-bit number to correctly address it.

Implementing a decoder
----------------------

The name of the game is **reduction**. Recall the maximum amount of memory addresses allowed by a 16-bit number (assuming all bits are '1'):

.. math::
   2^{16} = 65535

65536 unique addresses. The first 4-bits can be used to assign all addresses into chunks of size 4096-bits
which gives use 16 groups.

**0000** 000000000000

The next 3-bits can be used to assign the 4096-bits into chunks of size 512-bits which then gives us
8 groups.

0000 **000** 000000000

The last 9 bits can uniquely all 8 groups of size 512-bits.

0000000 **000000000**

Which gives us a unique binary number that is unambigous
for all 65536 values.


I haven't implemented the :ref:`ram` in a 'true' sense. I wanted to have ``64KB`` 
of Random Access Memory but the implementation of hard-coded RAM would be far-fetched
to run, let alone write. I opted to just use and array with ``read`` and ``write`` methods.

For fun, let's have a look at just the decoder truth tables:

**3-to-8 Decoder**

+---------+---+---+----+----+----+----+----+----+----+----+
| 2^3 = 8 |   |   |    |    |    |    |    |    |    |    |
+=========+===+===+====+====+====+====+====+====+====+====+
| A       | B | C | D0 | D1 | D2 | D3 | D4 | D5 | D6 | D7 |
+---------+---+---+----+----+----+----+----+----+----+----+
| 0       | 0 | 0 | 0  | 0  | 0  | 0  | 0  | 0  | 0  | 1  |
+---------+---+---+----+----+----+----+----+----+----+----+
| 0       | 0 | 1 | 0  | 0  | 0  | 0  | 0  | 0  | 1  | 0  |
+---------+---+---+----+----+----+----+----+----+----+----+
| 0       | 1 | 0 | 0  | 0  | 0  | 0  | 0  | 1  | 0  | 0  |
+---------+---+---+----+----+----+----+----+----+----+----+
| 0       | 1 | 1 | 0  | 0  | 0  | 0  | 1  | 0  | 0  | 0  |
+---------+---+---+----+----+----+----+----+----+----+----+
| 1       | 0 | 0 | 0  | 0  | 0  | 1  | 0  | 0  | 0  | 0  |
+---------+---+---+----+----+----+----+----+----+----+----+
| 1       | 0 | 1 | 0  | 0  | 1  | 0  | 0  | 0  | 0  | 0  |
+---------+---+---+----+----+----+----+----+----+----+----+
| 1       | 1 | 0 | 0  | 1  | 0  | 0  | 0  | 0  | 0  | 0  |
+---------+---+---+----+----+----+----+----+----+----+----+
| 1       | 1 | 1 | 1  | 0  | 0  | 0  | 0  | 0  | 0  | 0  |
+---------+---+---+----+----+----+----+----+----+----+----+

**4-to-16 Decoder**

+----------+---+---+---+---+---+---+---+---+---+---+---+---+---+----+----+----+----+----+----+
| 2^4 = 16 |   |   |   | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 |
+==========+===+===+===+===+===+===+===+===+===+===+===+===+===+====+====+====+====+====+====+
| 0        | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0  | 0  | 0  | 0  | 0  | 1  |
+----------+---+---+---+---+---+---+---+---+---+---+---+---+---+----+----+----+----+----+----+
| 0        | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0  | 0  | 0  | 0  | 1  | 0  |
+----------+---+---+---+---+---+---+---+---+---+---+---+---+---+----+----+----+----+----+----+
| 0        | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0  | 0  | 0  | 1  | 0  | 0  |
+----------+---+---+---+---+---+---+---+---+---+---+---+---+---+----+----+----+----+----+----+
| 0        | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0  | 0  | 1  | 0  | 0  | 0  |
+----------+---+---+---+---+---+---+---+---+---+---+---+---+---+----+----+----+----+----+----+
| 0        | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0  | 1  | 0  | 0  | 0  | 0  |
+----------+---+---+---+---+---+---+---+---+---+---+---+---+---+----+----+----+----+----+----+
| 0        | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1  | 0  | 0  | 0  | 0  | 0  |
+----------+---+---+---+---+---+---+---+---+---+---+---+---+---+----+----+----+----+----+----+
| 0        | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0  | 0  | 0  | 0  | 0  | 0  |
+----------+---+---+---+---+---+---+---+---+---+---+---+---+---+----+----+----+----+----+----+
| 0        | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0  | 0  | 0  | 0  | 0  | 0  |
+----------+---+---+---+---+---+---+---+---+---+---+---+---+---+----+----+----+----+----+----+
| 1        | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0  | 0  | 0  | 0  | 0  | 0  |
+----------+---+---+---+---+---+---+---+---+---+---+---+---+---+----+----+----+----+----+----+
| 1        | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0  | 0  | 0  | 0  | 0  | 0  |
+----------+---+---+---+---+---+---+---+---+---+---+---+---+---+----+----+----+----+----+----+
| 1        | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0  | 0  | 0  | 0  | 0  | 0  |
+----------+---+---+---+---+---+---+---+---+---+---+---+---+---+----+----+----+----+----+----+
| 1        | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0  | 0  | 0  | 0  | 0  | 0  |
+----------+---+---+---+---+---+---+---+---+---+---+---+---+---+----+----+----+----+----+----+
| 1        | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0  | 0  | 0  | 0  | 0  | 0  |
+----------+---+---+---+---+---+---+---+---+---+---+---+---+---+----+----+----+----+----+----+
| 1        | 1 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0  | 0  | 0  | 0  | 0  | 0  |
+----------+---+---+---+---+---+---+---+---+---+---+---+---+---+----+----+----+----+----+----+
| 1        | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0  | 0  | 0  | 0  | 0  | 0  |
+----------+---+---+---+---+---+---+---+---+---+---+---+---+---+----+----+----+----+----+----+

Next would be to map each of these values to specific memory locations each implementing a
`Register` object. INSANE!
