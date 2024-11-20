import random
import unicodedata
import re
from encoderfixed import encoderfixed
from decoderfixed import decoderfixed
from encodervariable import encodervariable
from decodervariable import decodervariable
from argparse import ArgumentParser
from os import path
import matplotlib.pyplot as plt

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

def plot_list(y,y_label,x_label,save_path,title):
    x = list(range(len(y)))
    plt.clf()
    plt.plot(x, y)
    
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    
    plt.savefig(save_path)

if __name__ == "__main__":
    parser = ArgumentParser()

    parser.add_argument("-filename", help="caminho do arquivo a ser comprimido/descomprimido")
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
        encoder = encodervariable(input=input_bitstr, initial_code_size=MAX_SIZE, stats=STATS)
        encoding, stats_encoding = encoder.encode()
        
        decoder = decodervariable(encoding=encoding, initial_code_size=MAX_SIZE, stats=STATS)
        decoding, stats_decoding = decoder.decode()
    else:
        encoder = encoderfixed(input=input_bitstr, codes_max_size=MAX_SIZE, stats=STATS)
        encoding, stats_encoding = encoder.encode()
        
        decoder = decoderfixed(encoding=encoding, code_size=MAX_SIZE, stats=STATS)
        decoding, stats_decoding = decoder.decode()
    if STATS:
        print("\n\n### Estatisticas da compressao: ###\n\n")
        print(f"tempo de codificacao: {stats_encoding['time']:.2f}") # taxa de bits da entrada que foram "pulados" por estarem representados por um codigo  
                                                # avaliada a cada 80 bits
        print("tamanho (em bits) do input:" + str(stats_encoding["input_size"]))                                        
        print("tamanho (em bits) apos encoding: " + str(stats_encoding["encoded_size"]))
        print("quantidade de codigos inseridos: " + str(stats_encoding["dict_size"]))
        print("\n\n####################################\n\n")
        # plot compression rate in here
        plot_list(y = stats_encoding["compression_rates"],
                    y_label = "taxa de compressao", x_label = "x80iteracoes",
                      save_path= (filepath + "_compression_rate.png"),
                      title="Analise da taxa de compressao")
            
        print("\n\n### Estatisticas da descompressao: ###\n\n")
        print(f"tempo de decodificacao (em segundos): {stats_decoding['time']:.2f}")
        print(f"quantidade de codigos usados: {stats_decoding['dict_size']}")
        print("\n\n####################################\n\n")
        print(stats_decoding["decompression_rates"][0:5])
        plot_list(y = stats_decoding["decompression_rates"],
                    y_label = "taxa de decompressao", x_label = "x50iteracoes",
                      save_path= (filepath + "_decompression_rate.png"),
                      title="Analise da taxa de descompressao")
        # taxa de bits decodificada por iteracao. avaliado a cada 50 iteracoes
