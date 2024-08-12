Logic Units (units.py)
======================

This page explains the inner logic gate setup of the =. To understand information on this page requires a basic understanding of 
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

The simplest method in which this is implemented in Python is:
I use the `&` binary operater as other solution involved **if**'s
which didn't seem as elegant.

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


16-Bit-Incrementer
******************

16-Bit-Subtracter
*****************


Switches
********
