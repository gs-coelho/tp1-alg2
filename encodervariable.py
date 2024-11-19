from dictionary import Dictionary

class encodervariable():
    def __init__(self, input: str, initial_code_size: int) -> None:
        self.__input = input
        self.__trie = Dictionary(initial0_key="0",initial0_value=0,
                                 initial1_key="1",initial1_value=1)
        self.__codes_count = 2
        self.__codes_bit_size = initial_code_size
        
    def encode(self):
        encoding = ""
        I = ""
        for i in self.__input:
            max_code = pow(2,self.__codes_bit_size)
            if self.__trie.search(I+i) != None:
                I = I + i
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
        
        print("codigos inseridos")
        print(self.__codes_count)
        return encoding