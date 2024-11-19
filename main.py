import random
import unicodedata
import re
from encoder import encoder, encoderold
#from decoder import decoder

def normalize_text(text):
    """
    Normalize text to remove accents and special characters.
    """
    # Normalize to NFD (decompose characters with accents)
    normalized = unicodedata.normalize('NFD', text)
    # Encode to ASCII, ignoring non-ASCII characters
    ascii_text = normalized.encode('ascii', 'ignore').decode('ascii')
    return ascii_text

def text_to_binary_string(file_path):
    """
    Read a text file, normalize it, and convert to a binary string.
    """
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Normalize the content
    normalized_content = normalize_text(content)
    
    # Convert normalized text to bytes
    byte_data = normalized_content.encode('ascii')  # Ensures ASCII encoding
    
    # Convert each byte to an 8-bit binary string and join
    binary_string = ''.join(f'{byte:08b}' for byte in byte_data)
    return binary_string

def file_to_binary_string(file_path):
    with open(file_path, 'rb') as image_file:
        binary_data = image_file.read()  # Read image as binary data
        binary_string = ''.join(format(byte, '08b') for byte in binary_data)  # Convert to binary string
    return binary_string

def random_binary_string(length):
    return ''.join(random.choices('01', k=length))




#INPUT_BYTES = 100000
#input_bitstr = random_binary_string(INPUT_BYTES*8) 
input_bitstr = text_to_binary_string("/home/victor/Projects/tp1-alg2/frankesteinfull.txt")
#print(input_bitstr)


encoder = encoder(input=input_bitstr,codes_max_size=16)
encoding = encoder.encode()


print("input size")
print(len(input_bitstr))
print("encoding size")
print(len(encoding))

# decoder = decoder(encoding=encoding)
# decoding = decoder.decode()

# print("decoding")
# print(decoding)

# if (decoding == input_bitstr):
#     print("deu certo")