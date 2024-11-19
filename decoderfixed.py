from dictionary import Dictionary

class decoderfixed():
    def __init__(self, encoding, code_size) -> None:
        self.__encoding = encoding
        zero_in_bin = bin(0)[2:].zfill(code_size)
        one_in_bin = bin(1)[2:].zfill(code_size)
        self.__table = Dictionary(initial0_key=zero_in_bin, initial0_value="0",
                                  initial1_key=one_in_bin, initial1_value="1")
        self.__code_size = code_size
        self.__code_count = 2
        self.__inserted_strs = Dictionary(initial0_key="0", initial0_value=0,
                                          initial1_key="1", initial1_value=0)
        
    def decode(self):
        decoding = ""
        previous_str = ""
        idx = 0
        while idx < len(self.__encoding):
            actual_code = self.__encoding[idx : idx+self.__code_size]
            if idx == 0:
                previous_str = self.__table.search(actual_code)
                idx += self.__code_size
                continue
            actual_str = self.__table.search(actual_code) 
            if (actual_str != None):# codigo na tabela
                if self.__inserted_strs.search(previous_str + actual_str[0]) == None:
                    code_in_binary = bin(self.__code_count)[2:].zfill(self.__code_size)
                    self.__table.insert(code_in_binary, previous_str + actual_str[0])
                    self.__inserted_strs.insert(previous_str + actual_str[0],0)
                    self.__code_count += 1
                # if(not_already_exists):
                #     print("isso aconteceu")
                decoding += previous_str
                previous_str = actual_str
            else:
                code_in_binary = bin(self.__code_count)[2:].zfill(self.__code_size)
                self.__table.insert(code_in_binary,previous_str + previous_str[0])
                self.__inserted_strs.insert(previous_str + previous_str[0],0)
                self.__code_count += 1
                decoding += previous_str
                previous_str = previous_str + previous_str[0]
    
            idx += self.__code_size
                            
        
        decoding += previous_str    
        return decoding
    
    
        
        # for idx, actual_code in enumerate(self.__encoding):
            
        #     if idx == 0:
        #         previous_str = self.__table[actual_code]
        #         continue
        #     if (0 <= actual_code < len(self.__table)):# codigo na tabela
        #         if (previous_str + self.__table[actual_code][0]) not in self.__table:
        #             self.__table.append(previous_str + self.__table[actual_code][0])
        #         decoding += previous_str
        #         previous_str = self.__table[actual_code]
        #     else:
        #         self.__table.append(previous_str + previous_str[0])
        #         decoding += previous_str
        #         previous_str = previous_str + previous_str[0]
            
            