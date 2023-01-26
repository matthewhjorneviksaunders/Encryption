import hashlib
import f2b
import gold
import numpy

IV = [1] * 256
K = [0, 1] * 128


def HashFucntion(K, M):

    key = f2b.bits_to_bytes(K)
    m = f2b.bits_to_bytes(M)
    hashed = hashlib.sha256(key + m).digest()

    return f2b.bytes_to_bits(hashed)


def BlockCipher(x, y):

    decrypt = False
    encrypt = False
    if y == 'decrypt':
        decrypt = True
    if y == 'encrypt':
        encrypt = True

    plaintext = f2b.read_file(x)
    Bits = list(f2b.bytes_to_bits(plaintext))
    if(len(Bits) < 256):
        for i in range(256 - len(Bits)):
            Bits.append(0)
    if(len(Bits) % 256 != 0):
        for i in range(256 - len(Bits) % 256):
            Bits.append(0)

    Blocks = [Bits[i:i+256] for i in range(0, len(Bits), 256)]
    encrypted = []

    for i in range(len(Blocks)):
        if(i == 0):
            encrypted.append(gold.xor(Blocks[i], HashFucntion(K, IV)))
        else:
            if encrypt == True:
                encrypted.append(
                    gold.xor(Blocks[i], HashFucntion(K, Blocks[i - 1])))
            elif decrypt == True:
                encrypted.append(
                    gold.xor(Blocks[i], HashFucntion(K, encrypted[i - 1])))

    byteSeq = numpy.packbits(encrypted)
    f = open('sha256.out', 'wb')
    f.write(byteSeq)
    f.close()


def Main():

    x = input('Filename: ').lower()
    y = input('Encrypt or Decrypt?: ').lower()
    BlockCipher(x, y)


Main()
