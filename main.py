import random
import unicodedata
import re
from encoderfixed import encoderfixed, encoderold
from decoderfixed import decoderfixed
from argparse import ArgumentParser
from os import path

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
    with open(file_path, 'rb') as file:
        binary_data = file.read()  # Read file as binary data
        binary_string = ''.join(format(byte, '08b') for byte in binary_data)  # Convert to binary string
    return binary_string

def binary_string_to_file(file_path, binary_string):
    with open(file_path, 'rb') as file:
        binary_data = file.read()  # Read image as binary data
        binary_string = ''.join(format(byte, '08b') for byte in binary_data)  # Convert to binary string
    return binary_string

def random_binary_string(length):
    return ''.join(random.choices('01', k=length))

if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument("filename", help="caminho do arquivo a ser comprimido/descomprimido")
    parser.add_argument("-s", "--stats", action="store_true", help="gera estatísticas da compressão/decompressão")
    parser.add_argument("-v", "--variable", action="store_true", help="executa a compressão LZW com tamanho de código variável, ao invés de tamanho fixo (padrão)")
    parser.add_argument("-m", "--maxsize", nargs="?", const=12, default=12, help="tamanho máximo de código", type=int)

    args = parser.parse_args()
    FILENAME = args.filename
    STATS = args.stats
    VARIABLE = args.variable
    MAX_SIZE = args.maxsize

    input_file_path = path.realpath(path.expanduser(FILENAME))
    filepath, ext = path.splitext(input_file_path)
    encoded_file_path = filepath + "_encoded"
    decoded_file_path = filepath + "_decoded" + ext

    input_bitstr = file_to_binary_string(input_file_path)

    if VARIABLE:
        pass
    else:
        encoder = encoderfixed(input=input_bitstr, codes_max_size=MAX_SIZE)
        encoding = encoder.encode()
        decoder = decoderfixed(encoding=encoding, code_size=MAX_SIZE)
        decoding = decoder.decode()

        if (decoding == input_bitstr):
            print("deu certo")


# print("input size")
# print(len(input_bitstr))
# print("encoding size")
# print(len(encoding))


# print("decoding")
# print(decoding)
