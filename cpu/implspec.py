# **MIT LICENSE**

def pushToTuple(array, bits):
    """

    :param [] array: Preinitialised array of size n.
    :param int bits: Binary number of size n.

    :return: Tuple-Binary of type tuple.
    """
    bits = [int(bit) for bit in bin(bits)[2:]][::-1]
    for index, _ in enumerate(bits):
        array[index] = bits[index]
    return tuple(array)

def generate4Bits(bits4 = 0b0):
    """
    :param int bits: Binary number of size 4.

    :return: Tuple-Binary of type tuple.
    """
    nibble = [0, 0, 0, 0]
    return pushToTuple(nibble, bits4)

def generate8Bits(bits8 = 0b0):
    """
    :param int bits: Binary number of size 8.

    :return: Tuple-Binary of type tuple.
    """
    byte = [0, 0, 0, 0, 0, 0, 0, 0]
    return pushToTuple(byte, bits8)

def generate16Bits(bits16 = 0b0):
    """
    :param int bits: Binary number of size 16.

    :return: Tuple-Binary of type tuple.
    """
    two_bytes = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    return pushToTuple(two_bytes, bits16)

def generateStreamBits(bit):
    """
    :param int bit: Binary digit.

    :return: 16-bits of inputed bit of type int.
    """
    # This function is needed because of the 
    # implentation of generate16Bits
    if bit == 1:
        return 0b1111111111111111
    else:
        return 0b0000000000000000

def tupleToBinary(tuple_binary):
    """
    :param () tuple: A Tuple-Binary value.

    :return: 16-bit number of type int.
    """
    return int(''.join([str(value) for value in tuple_binary]), 2)


def isLessThanZero(tuple_binary):
    """
    :param () tuple: A Tuple-Binary value.

    :return: 1st bit of tuple of type int.
    """
    return tuple_binary[0]


# DEPRECATED
def decimalToBinary(integer):
    return int(bin(integer)[2:], 2)
def reverseBits(tuple_binary):
    return tuple_binary[::-1]

