Logic Units (units.py)
======================

This page explains the inner logic gate setup of the Arithmetic and Logic Unit. To understand information on this page requires a basic understanding of 
truth tables and logic gates.
 

.. _logic-gates:

Logic Gates
***********

This is the most fundemental section in the CPU. All logic gates can be
derived from the **NAND** gate.

NAND GATE
---------

+---+---+-----+
| A | B | OUT |
+===+===+=====+
| 0 | 0 | 1   |
+---+---+-----+
| 0 | 1 | 1   |
+---+---+-----+
| 1 | 0 | 1   |
+---+---+-----+
| 1 | 1 | 0   |
+---+---+-----+

The simplest way in which this is implemented in Python is:

Is the use of the `&` binary operater:

.. math::
   bit = -1 \cdot (int(a \& b) - 1)


INVERTED GATE
-------------

This gate can be created by taking NAND where a is both a and b.

+---+-----+
| A | OUT |
+===+=====+
| 0 | 1   |
+---+-----+
| 1 | 0   |
+---+-----+


AND GATE
--------

The AND gate is an inverted NAND.

+---+---+-----+
| A | B | OUT |
+===+===+=====+
| 0 | 0 | 0   |
+---+---+-----+
| 0 | 1 | 0   |
+---+---+-----+
| 1 | 0 | 0   |
+---+---+-----+
| 1 | 1 | 1   |
+---+---+-----+

OR GATE
-------

The OR gate is created by inverting both inputs then passing
the inverted inputs into a NAND gate.

+---+---+-----+
| A | B | OUT |
+===+===+=====+
| 0 | 0 | 0   |
+---+---+-----+
| 0 | 1 | 1   |
+---+---+-----+
| 1 | 0 | 1   |
+---+---+-----+
| 1 | 1 | 1   |
+---+---+-----+


EXCLUSIVE OR GATE (XOR)
-----------------------

The XOR gate descriminates based on the input side. To create
one, inputs are fed into a NAND gate. The output of this gate
is discriminated against the NAND of either A or B where the
final bit is then inverted in and AND.


+---+---+-----+
| A | B | OUT |
+===+===+=====+
| 0 | 0 | 0   |
+---+---+-----+
| 0 | 1 | 1   |
+---+---+-----+
| 1 | 0 | 1   |
+---+---+-----+
| 1 | 1 | 0   |
+---+---+-----+


16-Bit Variants
---------------

Implementing a 16-bit versions of the logic gates is as simple as taking
two 16-bit binary numbers and comparing each index of each value with a
respective logic gate. Look in `units.py` at line 40 to see the implementation.

A `16` in the signature means that method uses 16-bit numbers.


Half-Adder
**********

The Half-Adder is a logical unit that adds two bits together. This will allow
us to get a maximum value of 3:

.. math::
   2^{2} -1 = 3

A Half-Adder will produce a **high** and **low** bit. Where high is 1 if both values
are 1 (1 + 1 = 2 which is ``0b10`` in binary). Which can be constructed by process
of elimination of bits.

**HALF-ADDER TRUTH TABLE**

+---+---+------+-----+
| A | B | HIGH | LOW |
+===+===+======+=====+
| 0 | 0 | 0    | 0   |
+---+---+------+-----+
| 0 | 1 | 0    | 1   |
+---+---+------+-----+
| 1 | 0 | 0    | 1   |
+---+---+------+-----+
| 1 | 1 | 1    | 0   |
+---+---+------+-----+

Full-Adder
**********

A Full-Adder are two Half-Adders linked together where the value is `allowed` to overflow.
This overflow is called a carry indicating that the number it too large to fit in the
current buffer.

The Full-Adder takes in three bits; A, B, Carry. And will produce a **high** and **low** bit.

**FULL-ADDER TRUTH TABLE**

+---+---+-------+------+-----+
| A | B | CARRY | HIGH | LOW |
+===+===+=======+======+=====+
| 0 | 0 | 0     | 0    | 0   |
+---+---+-------+------+-----+
| 0 | 0 | 1     | 0    | 1   |
+---+---+-------+------+-----+
| 0 | 1 | 0     | 0    | 1   |
+---+---+-------+------+-----+
| 0 | 1 | 1     | 1    | 0   |
+---+---+-------+------+-----+
| 1 | 0 | 0     | 0    | 0   |
+---+---+-------+------+-----+
| 1 | 0 | 1     | 1    | 0   |
+---+---+-------+------+-----+
| 1 | 1 | 0     | 1    | 0   |
+---+---+-------+------+-----+
| 1 | 1 | 1     | 1    | 1   |
+---+---+-------+------+-----+


Multi-Bit-Adder
***************

The Multi-Bit-Adder are two or more Full-Adders linked where the carry bit of
the previous Full-Adder is piped into the current Full-Adder; unless it's the
last adder, in-that-case the bit is dropped.

**MULTI-BIT-ADDER TRUTH TABLE**

These are all the possible inputs for two 2-bit numbers and a 1-bit number.

+----+----+----+----+-------+
| A1 | A2 | B1 | B2 | CARRY |
+====+====+====+====+=======+
| 0  | 0  | 0  | 0  | 0     |
+----+----+----+----+-------+
| 0  | 0  | 0  | 0  | 1     |
+----+----+----+----+-------+
| 0  | 1  | 0  | 1  | 0     |
+----+----+----+----+-------+
| 0  | 1  | 0  | 1  | 1     |
+----+----+----+----+-------+
| 1  | 0  | 1  | 0  | 0     |
+----+----+----+----+-------+
| 1  | 0  | 1  | 0  | 1     |
+----+----+----+----+-------+
| 1  | 1  | 1  | 1  | 0     |
+----+----+----+----+-------+
| 1  | 1  | 1  | 1  | 1     |
+----+----+----+----+-------+

**DATA BREAKDOWN**

The maximum value of a 3-bit number is 7;

.. math::
   2^{3} -1 = 7

The binary number is being broken-down into individual
bits sorted right to left starting at O2. The decimal
header is there to help understand the numbering.

**O1** is the expected output for the low bits

**O2** is the expected output for the high bits

**CARRY** is the expected carry output.

+------------------------+---------+-------+----+----+
| SUM OF ALL 3 in binary | DECIMAL | CARRY | O1 | O2 |
+========================+=========+=======+====+====+
| 0                      | 0       | 0     | 0  | 0  |
+------------------------+---------+-------+----+----+
| 1                      | 1       | 0     | 0  | 1  |
+------------------------+---------+-------+----+----+
| 10                     | 2       | 0     | 1  | 0  |
+------------------------+---------+-------+----+----+
| 11                     | 3       | 0     | 1  | 1  |
+------------------------+---------+-------+----+----+
| 100                    | 4       | 1     | 0  | 0  |
+------------------------+---------+-------+----+----+
| 101                    | 5       | 1     | 0  | 1  |
+------------------------+---------+-------+----+----+
| 110                    | 6       | 1     | 1  | 0  |
+------------------------+---------+-------+----+----+
| 111                    | 7       | 1     | 1  | 1  |
+------------------------+---------+-------+----+----+

**This table then corresponds with the following output below**

First we add the low bits. If there are any carry bits add
these to the high bits. If there is an overflow change the bit
to 1.

Output all low bits because the values will not change if more numbers
are added.

+---------------------------+----------+------------------------------------+----------+
| Low bit sum = A2+B2+CARRY |          | High bit sum = A1+B1+(Low bit sum) |          |
+===========================+==========+====================================+==========+
| HIGH                      | LOW - O2 | HIGH - CARRY OUT                   | LOW - O1 |
+---------------------------+----------+------------------------------------+----------+
| 0                         | 0        | 0                                  | 0        |
+---------------------------+----------+------------------------------------+----------+
| 0                         | 1        | 0                                  | 0        |
+---------------------------+----------+------------------------------------+----------+
| 1                         | 0        | 0                                  | 1        |
+---------------------------+----------+------------------------------------+----------+
| 1                         | 1        | 0                                  | 1        |
+---------------------------+----------+------------------------------------+----------+
| 0                         | 0        | 1                                  | 0        |
+---------------------------+----------+------------------------------------+----------+
| 0                         | 1        | 1                                  | 0        |
+---------------------------+----------+------------------------------------+----------+
| 1                         | 0        | 1                                  | 1        |
+---------------------------+----------+------------------------------------+----------+
| 1                         | 1        | 1                                  | 1        |
+---------------------------+----------+------------------------------------+----------+

16-Bit-Adder
************

The 16-Bit-Adder functions in the same way the Multi-Bit-Adder works; where the
high bit is carried over from the previous Full-Adder. Chaining 16 Full-Adders
together gives you a 16-Bit-Adder. The last high value is dicarded.


To use the ``BitAdder16`` class call it's method ``add``.

It takes in two `16-bit binary number` arguments.

The return value is the added result `16-bit tuple result`.

.. code-block::
    
   bitadder_16.add(0b11, 0b101)
   Output: (0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1)

.. ATTENTION::
   The output of the basic 16-bit units will return tuple values as
   it keeps the virtual pins seperate.
   A utility function is implemented to convert tuples to binary values.
   :ref:`tuple-to-binary`

.. _increment-16:

16-Bit-Incrementer
******************

A 16-bit increment can be built be connecting a 16-Bit-Adder to a constant signal; `1`.
Then we need to take in a 16-bit binary number (`optionally`) to tell the incrementer
where to start.

To use the ``Incremenet16`` class call it's method ``inc``.

It takes in an `optional` argument of a `16-bit binary number`.

The return value is the `incremented tuple value`.

.. HINT::
   A full 16-bit number is not required. The ``inc`` method implements the ``BitAdder16``
   class which implements 16 Full-Adders. If you recall, there is a utility function in
   this method to generate 16 bits where the bits are n < 17.

.. code-block::
    
   increment_16.inc()
   Output: (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1)

   increment_16.inc(0b101)
   Output: (0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0)



16-Bit-Subtracter
*****************

The 16-Bit-Subtracter subtracts two 16-bit numbers. It supports negative numbers.
If a binary number starts with a '1' that signals that this binary number is negative.
This is known as "Two's Complement" (Learn more about `Two's Complement`_)

   .. _Two's Complement: https://en.wikipedia.org/wiki/Two%27s_complement


In order to implement this method we need follows:

.. math::
   a - b = c \implies -(a - b) = -c

.. math::
    -(a-b) = -c \implies (-a)+b = -c 

.. math::
    (-a)+b = -c \implies a + (-b) = c

From the equation above we need an `inverted` number `added` to a normal binary number.

.. `1-bit is
.. is added to account for the for the high bit in the inverted number (A.K.A Two's Complement)`

**SUBTRACTION TRUTH TABLE**

+----+----+-------+---------------+
| A  | B  | NOT B | A + NOT B + 1 |
+====+====+=======+===============+
| 01 | 01 | 10    | 00            |
+----+----+-------+---------------+
| 01 | 00 | 11    | 01            |
+----+----+-------+---------------+
| 10 | 11 | 00    | 11            |
+----+----+-------+---------------+
| 11 | 10 | 01    | 01            |
+----+----+-------+---------------+

The high bit (most significant bit) indicates if the number is negative.


To use the ``Subtract16`` class call it's method ``sub``.

It takes in the `16-bit binary number` arguments.

The return value is the subtracted result `16-bit tuple result`.

.. code-block::
    
   subract_16.sub(0b10, 0b1)
   Output: (0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1)

   subtract_16.inc(0b11, 0b100)
   Output: (1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1)

.. _stream-bits:
   
Switches
********

A `switch` is required to choose between different inputs and outputs.

The ``select`` method in the ``Switch`` class controls which input to choose.
This is done by `inverting` the first stream then discriminating against each
input. Although callable, the single bit ``select`` should not be used directly; opt
in to using the 16 bit variant.

The 16-bit variant of ``select`` is called ``select_16`` and requires to 16-bit
binary values and a 1-bit stream value.

The arguments required are two `16-bit binary numbers` and a one `1-bit stream bit`.

The return value of the 16-bit variant is a `16-bit binary number`.

.. ATTENTION::
   Due the implementation of the :ref:`generate-bits` utility function, the stream
   bit needs to be 16-bits long therefore the stream bit it used to generate
   16 stream bits using the ``generateStreamBits`` function.


Logic Unit
**********

A `Logic Unit` determines various `truths` or `outputs` of supplied values.

+-----+-----+----------+
| OP1 | OP2 | OUTPUT   |
+=====+=====+==========+
| 0   | 0   | X and Y  |
+-----+-----+----------+
| 0   | 1   | X or Y   |
+-----+-----+----------+
| 1   | 0   | X xor Y  |
+-----+-----+----------+
| 1   | 1   | invert X |
+-----+-----+----------+

To use the ``LogicUnit`` class call it's method ``calc``.

It takes in two `16-bit binary number` arguments and two `operation codes`.

The return result is a `16-bit binary number`.

.. code-block::
    
   logic_unit.calc(0, 0, 0b1, 0b1)
   Output: 1

   logic_unit.calc(0, 1, 0b11, 0b100)
   Output: 7

   logic_unit.calc(1, 1, 0b100, 0b0)
   Output: 65531

.. HINT::
   The output values are **numbers**. The representation does not matter.
   Python will display them as base-10 decimal. The only thing that matters
   with the output is that it is of type **int** (meaning it is an instance of the
   base integer class in Python).

Arithmetic Unit
***************

The `Arithmetic Unit` functions in much the same way as the `Logic Unit`
except it's `opcodes` correspond to different actions.

+-----+-----+--------+
| OP1 | OP2 | OUTPUT |
+=====+=====+========+
| 0   | 0   | X + Y  |
+-----+-----+--------+
| 0   | 1   | X - Y  |
+-----+-----+--------+
| 1   | 0   | X - 1  |
+-----+-----+--------+
| 1   | 1   | X - 1  |
+-----+-----+--------+

To use the ``ArithmeticUnit`` class call it's method ``calc``.

It takes in two `16-bit binary number` arguments and two `operation codes`.

The return result is a `16-bit binary number`.

.. code-block::
    
   arithmetic.calc(0, 0, 0b101, 0b100)
   Output: 9

   arithmetic.calc(1, 0, 0b101, 0b100)
   Output: 1


.. _alu:

ALU
***

The `ALU` stands for `Arithmetic and Logic Unit`. As you may have guessed, this
combines the functionality of the `Arithmetic Unit` and the `Logic Unit`.

This is done by using the ``Switch`` class method ``select_16``.

+---------------------+-----+-----+---------+---------+----------+
| Arithmetic or Logic | OP1 | OP2 | 16-bits | 16-bits | OUTPUT   |
+=====================+=====+=====+=========+=========+==========+
| 0                   | 0   | 0   | ANY     | ANY     | X AND Y  |
+---------------------+-----+-----+---------+---------+----------+
| 0                   | 0   | 1   | ANY     | ANY     | X OR Y   |
+---------------------+-----+-----+---------+---------+----------+
| 0                   | 1   | 0   | ANY     | ANY     | X XOR Y  |
+---------------------+-----+-----+---------+---------+----------+
| 0                   | 1   | 1   | ANY     | ANY     | INVERT X |
+---------------------+-----+-----+---------+---------+----------+
| 1                   | 0   | 0   | ANY     | ANY     | X + Y    |
+---------------------+-----+-----+---------+---------+----------+
| 1                   | 0   | 1   | ANY     | ANY     | X - Y    |
+---------------------+-----+-----+---------+---------+----------+
| 1                   | 1   | 0   | ANY     | ANY     | X + 1    |
+---------------------+-----+-----+---------+---------+----------+
| 1                   | 1   | 1   | ANY     | ANY     | X - 1    |
+---------------------+-----+-----+---------+---------+----------+

A `zero-replace` and `swap` are added in. 

  - **Swap**, switch the places of X and Y
  - **Zero-Replace**, switches the output of the first operand to 0

It takes in two `16-bit binary number` arguments, **four** `operation codes`, and one `1-bit stream bit`
to choose between the `Logic Unit` and the `Arithmetic Unit`.

The return result is a `16-bit binary number`.

.. code-block::

   # alu.calc(logic_or_arith, op1, op2, zero_replace, swap, binary_number, binary_number)

   alu.calc(1, 1, 0, 0, 0, 0b11, 0b1)
   Output: 2

   alu.calc(0, 1, 1, 0, 0, 0b0, 0b0)
   Output: 65535

.. _direct-a-register-write:

Conditional Unit
****************

The `Conditional Unit` checks if a 16-bit binary number is:
  
  - Less than zero
  - Greater than zero
  - Equal to zero

or any combination in-between. Whether or not the condition is
true will influence the :ref:`program-counter` starting value (if
the value is 1 then the current address at `reigster 'a'` is used
as the starting value).
