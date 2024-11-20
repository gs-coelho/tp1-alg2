# Encoder/Decoder 
from encoderfixed import encoderfixed
from decoderfixed import decoderfixed
from encodervariable import encodervariable
from decodervariable import decodervariable

# Command-line argument parsing
from argparse import ArgumentParser
from os import path

# Binary I/O
from binary_io import *

# Graphics and plotting
import matplotlib.pyplot as plt


def plot_list(y,y_label,x_label,save_path,title):
    x = list(range(len(y)))
    plt.clf()
    plt.plot(x, y)
    
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    
    plt.savefig(save_path)
    
if __name__ == "__main__":
    # Command-line argument parsing
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

    # Defining filepaths to be used in the program
    input_file_path = path.realpath(path.expanduser(FILENAME))
    filepath, ext = path.splitext(input_file_path)
    encoded_file_path = filepath + "_encoded" + ".lzw"
    decoded_file_path = filepath + "_decoded" + ext


    input_bitstr = file_to_binary_string(input_file_path)

    if VARIABLE:
        EncoderClassVar = encodervariable
        DecoderClassVar = decodervariable
    else:
        EncoderClassVar = encoderfixed
        DecoderClassVar = decoderfixed
        # CR: media da quantidade de bits gerados a partir da codificacao a cada 50 iteracoes
        # print(stats["decompression_rates"][0:5])

    # Compresses file and stores in binary file
    encoder_params = {
        "input": input_bitstr,
        "initial_code_size" if VARIABLE else "codes_max_size": MAX_SIZE,
        "stats": STATS
    }
    encoder = EncoderClassVar(**encoder_params)
    encoded_bitstr, stats_encoding = encoder.encode()
    binary_string_to_file(encoded_file_path, encoded_bitstr, signal_alignment=True)

    # Reads back from file, decompresses it and stores in original format
    encoded_bitstr_from_file = file_to_binary_string(encoded_file_path, alignment_signal=True)
    decoder_params = {
        "encoding": encoded_bitstr_from_file,
        "initial_code_size" if VARIABLE else "code_size": MAX_SIZE,
        "stats": STATS
    }
    decoder = DecoderClassVar(**decoder_params)
    decoded_bitstr, stats_decoding = decoder.decode()
    binary_string_to_file(decoded_file_path, decoded_bitstr, signal_alignment=False)

    if input_bitstr == decoded_bitstr:
        print("Arquivo original e final correspondem. Tudo certo!")
    else:
        print("Ocorreu um erro: arquivo original e final não correspondem.")

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
