Implementation Specific (implspec.py)
=====================================


This page contains information about the :ref:`utility`
needed to operate the CPU such as generating bits, inverting bits,
bit and reading bits.

.. _utility:

Utility Functions
*****************

These functions exist due the the implementation in Python and to
make testing the functions and methods easier. The logic remains
the same without these functions.

Push to Tuple
-------------

`Push to tuple` takes in an `n` sized array of binary values and
creates a tuple of binary values **Tuple-binary**.

.. autofunction:: implspec.pushToTuple
   :no-index:

.. TIP::
   The bits are reversed to make trailing zeros important
   For example: ``1,0,0, 0...`` is 4 (in binary) but will not be recognised
   because when pushed to the tuple it will be ``(...,0,0,1)`` is 
   which means 1 (in binary). When reversed: ``0,0,1,...`` and pushed
   to a tuple it will be ``(0,0,1,...)``

.. HINT::
   Tuple-binary values are always in reverse binary order. Where the 
   left most bit is the least and the vice-versa.

.. _generate-bits:

Generate X Bits
---------------

Generator function exists to make writing tests and inputs easier. Without
this function I would have to `'cheat'` in a sense and use string subscripting
with integer conversion.

There are `4`, `8` and `16` bit generators.

They take in a one `n-bit binary number` (where n < specified-bit).  

Returns a tuple-binary of size `n`.

.. code-block::

  generate8Bits(0b10)
  Output: (0,1,0,0,0,0,0,0)

  generate16Bits(0b10)
  Output: (0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0)

Generate Stream Bits
--------------------

Due the implementation of the :ref:`generate-bits`, the 16-bit variant of :ref:`stream-bits`
needs to be of size 16.

Where the function does this:

.. code-block::

    if bit == 1:
        return 0b1111111111111111
    else:
        return 0b0000000000000000

Call the function ``generateStreamBits`` and provide one 1-bit value.

.. code-block::
    
    generateStreamBits(1)
    Output: 65535 # decimal representation

.. _tuple-to-binary:

Tuple to Binary
---------------

Tuple-to-binary takes in a tuple-binary of size `n` and produces
a value of size `n` in an integer representation (it will be of type ``int``
in Python).

The argument supplied is the `tuple-binary`.

The return value is an `integer`.

.. code-block::
    
    tupleToBinary((1,0))
    Output: 2 # decimal representation

.. Decimal to Binary
.. -----------------
..
.. Decimal-to-binary takes in a decimal number

Less Than Zero
--------------

In order to determine if a number is negative (less than zero) the 16th
bit is read. If it's 1 then the number is negative.

The argument supplied is the `tuple-binary`.

The return value is an `integer`, 1 if its true, zero if false.

.. code-block::

   isLessThanZero((1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0))
   Output: 1

   isLessThanZero((0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1))
   Output: 0
..
.. Reverse Bits
.. ------------
..
.. Reverse-bits reverses the order of the supplied tuple-binary.
..
.. The argument supplied is the `tuple-binary`.
..
.. The return value is the reversed `tuple-binary`.
