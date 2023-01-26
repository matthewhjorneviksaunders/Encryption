import gold
import f2b

# Output size = 32
# Complexity of 2^n/2, where n is the output length. With current hashfunction it would take 2^16 computations to find a pair of inputs with same hash.


def HashFunction():

    plaintext = f2b.read_file('gold_plaintext.in')
    Bits = f2b.bytes_to_bits(plaintext)

    if(len(Bits) < 32):
        for i in range(32 - len(Bits)):
            Bits.append(0)
    if(len(Bits) % 32 != 0):
        for i in range(32 - len(Bits) % 32):
            Bits.append(0)

    Blocks = [Bits[i:i+32] for i in range(0, len(Bits), 32)]

    currentValue = [1] * 32

    for i in Blocks:

        currentValue = gold.xor(gold.encrypt(i, currentValue), i)

    return currentValue


print(HashFunction())
