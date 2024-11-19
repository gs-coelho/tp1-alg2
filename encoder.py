from dictionary import Dictionary

class encoder():
    def __init__(self, input: str, codes_max_size: int) -> None:
        self.__input = input
        self.__trie = Dictionary(initial_code_size=codes_max_size)
        self.__codes_count = 2
        self.__codes_bit_size = codes_max_size
        
    def encode(self):
        encoding = ""
        I = ""
        max_code = pow(2,self.__codes_bit_size)
        for i in self.__input:
            if self.__trie.search(I+i) != None:
                I = I + i
            else:
                if self.__codes_count < max_code: # ainda nao estourei o numero de codigos
                    self.__trie.insert(I+i,self.__codes_count)
                    self.__codes_count += 1
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
    
    
class encoderold():
    def __init__(self, input: str, code_max_bits) -> None:
        self.__input = input
        self.__trie = {"0": 0, "1": 1}
        self.__codes_count = 2
        self.__code_max_bits = code_max_bits
        
    def encode(self):
        encoding = ""
        I = ""
        limit = pow(2,self.__code_max_bits)
        for i in self.__input:
            if (I + i) in self.__trie:
                I = I + i
            else:
                if self.__codes_count < limit:
                    self.__trie[I+i] = self.__codes_count
                    self.__codes_count += 1
                code_in_binary = bin(self.__trie[I])[2:].zfill(self.__code_max_bits)
                encoding+=code_in_binary
                I = i
        
        if I != "":
            code_in_binary = bin(self.__trie[I])[2:].zfill(self.__code_max_bits)
            encoding += code_in_binary
        
        return encoding