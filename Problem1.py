import gold
import numpy


def FileToBits(x):

    Bytes = numpy.fromfile(x, dtype='uint8')
    Bits = numpy.unpackbits(Bytes)
    Bits = list(Bits)
    if(len(Bits) % 32 != 0):
        for i in range(32 - len(Bits) % 32):
            Bits.append(0)
    if(len(Bits) < 32):
        for i in range(32 - len(Bits)):
            Bits.append(0)
    return Bits


def ECB(x, K):

    encrypted = []
    plaintextBlocks = numpy.array_split(x, len(x)/32)
    blocks = []

    for i in plaintextBlocks:
        blocks.append(list(i))

    for i in blocks:
        encrypted.append(gold.encrypt(i, K))

    return encrypted


def CBC(x, K):

    encrypted = []
    plaintextBlocks = numpy.array_split(x, len(x)/32)
    blocks = []
    IV = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
          1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

    for i in plaintextBlocks:
        blocks.append(list(i))

    for i in blocks:
        c = gold.encrypt(gold.xor(i, IV), K)
        encrypted.append(c)
        IV = c

    return encrypted


def OFB(x, K):

    IV = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
          1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    encrypted = []
    plaintextBlocks = numpy.array_split(x, len(x)/32)
    blocks = []

    for i in plaintextBlocks:
        blocks.append(list(i))

    for i in blocks:
        x = gold.encrypt(IV, K)
        IV = x
        encrypted.append(gold.xor(i, x))

    return encrypted


def Main():

    K = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1,
         0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
    plaintext = FileToBits('gold_plaintext.in')
    ecb = ECB(plaintext, K)
    byteSeqEcb = numpy.packbits(ecb)
    cbc = CBC(plaintext, K)
    byteSeqCbc = numpy.packbits(cbc)
    ofb = OFB(plaintext, K)
    byteSeqOfb = numpy.packbits(ofb)

    e = open('out.ecb', 'wb')
    c = open('out.cbc', 'wb')
    o = open('out.ofb', 'wb')
    e.write(byteSeqEcb)
    c.write(byteSeqCbc)
    o.write(byteSeqOfb)
    e.close()
    c.close()
    o.close()


Main()
