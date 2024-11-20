from dictionary import Dictionary
import time

class encodervariable():
    def __init__(self, input: str, initial_code_size: int, stats: bool, max_code_size:int = 30) -> None:
        self.__input = input
        self.__trie = Dictionary(initial0_key="0",initial0_value=0,
                                 initial1_key="1",initial1_value=1)
        self.__codes_count = 2
        self.__codes_bit_size = initial_code_size
        if stats:
            self.__stats = {"compression_rates":[],
                            "dict_size":None,
                            "time":None,
                            "input_size": len(self.__input),
                            "encoded_size": None
                            }
        else:
            self.__stats = None
        
    def encode(self):
        encoding = ""
        I = ""
        count_compressions = 0
        start_time = time.time()
        for idx, i in enumerate(self.__input):
            if(self.__stats != None and idx > 0 and idx % 80 == 0):
                self.__stats["compression_rates"].append(count_compressions/80)
                count_compressions = 0
            max_code = pow(2,self.__codes_bit_size)
            if self.__trie.search(I+i) != None:
                I = I + i
                count_compressions += 1
            else:
                estourou = False
                if self.__codes_count == max_code-1: # estourei o numero de codigos
                    estourou = True
                    Icode_in_binary = bin(self.__trie.search(I))[2:].zfill(self.__codes_bit_size)
                    encoding+=Icode_in_binary
                    ones = bin(pow(2,self.__codes_bit_size) - 1)[2:]
                    encoding += ones
                    self.__codes_bit_size += 1
                    self.__codes_count += 1
                self.__trie.insert(I+i,self.__codes_count)
                self.__codes_count += 1
                if not estourou: # caso nao tenha entrado acima
                    code = self.__trie.search(I)
                    code_in_binary = bin(code)
                    code_in_binary = code_in_binary[2:]
                    code_in_binary = code_in_binary.zfill(self.__codes_bit_size)
                    encoding+=code_in_binary
                I = i
        
        if I != "":
            code_in_binary = bin(self.__trie.search(I))[2:].zfill(self.__codes_bit_size)
            encoding+=code_in_binary
        end_time = time.time()
        if self.__stats != None:
            self.__stats["time"] = end_time - start_time
            self.__stats["dict_size"] = self.__codes_count
            self.__stats["encoded_size"] = len(encoding)
        return encoding, self.__stats