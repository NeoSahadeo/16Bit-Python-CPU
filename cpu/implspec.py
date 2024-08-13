# **MIT LICENSE**

# All functions in this file are implementation specific
# that being they are needed only in THIS Python 16bit CPU

def pushToTuple(array, bits):
    bits = [int(bit) for bit in bin(bits)[2:]][::-1]
    for index, _ in enumerate(bits):
        array[index] = bits[index]
    return tuple(array)

def generate4Bits(bit4 = 0b0):
    nibble = [0, 0, 0, 0]
    return pushToTuple(nibble, bit4)

def generate8Bits(bit8 = 0b0):
    byte = [0, 0, 0, 0, 0, 0, 0, 0]
    return pushToTuple(byte, bit8)

def generate16Bits(bit16 = 0b0):
    two_bytes = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    return pushToTuple(two_bytes, bit16)

def generateStreamBits(bit):
    # This function is needed because of the 
    # implentation of generate16Bits
    if bit == 1:
        return 0b1111111111111111
    else:
        return 0b0000000000000000

def tupleToBinary(tuple_binary):
    return int(''.join([str(value) for value in tuple_binary]), 2)

def decimalToBinary(integer):
    return int(bin(integer)[2:], 2)

def isLessThanZero(tuple_binary):
    return tuple_binary[0]

def reverseBits(tuple_binary):
    return tuple_binary[::-1]

