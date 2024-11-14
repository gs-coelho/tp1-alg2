import random
from encoder import encoder
from decoder import decoder

def random_binary_string(length):
    return ''.join(random.choices('01', k=length))

INPUT_BYTES = 8

input_bitstr = random_binary_string(INPUT_BYTES*8)
# input_bitstr = "0000011110110011111000000110011100100100001100000000100101011101"

encoder = encoder(input=input_bitstr)
encoding = encoder.encode()

print(input_bitstr)
print(encoding)
print(len(encoding))

decoder = decoder(encoding=encoding)
decoding = decoder.decode()

print("decoding")
print(decoding)