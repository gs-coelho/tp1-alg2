from dictionary import Dictionary
import time

class decoderfixed():
    def __init__(self, encoding, code_size, stats: bool) -> None:
        self.__encoding = encoding
        zero_in_bin = bin(0)[2:].zfill(code_size)
        one_in_bin = bin(1)[2:].zfill(code_size)
        self.__table = Dictionary(initial0_key=zero_in_bin, initial0_value="0",
                                  initial1_key=one_in_bin, initial1_value="1")
        self.__code_size = code_size
        self.__code_count = 2
        self.__inserted_strs = Dictionary(initial0_key="0", initial0_value=0,
                                          initial1_key="1", initial1_value=0)
        if stats:
            self.__stats = {"decompression_rates":[],
                            "dict_size":None,
                            "time":None,
                            }
        else:
            self.__stats = None
        
    def decode(self):
        decoding = ""
        previous_str = ""
        idx = 0
        it = 0
        decompressing_acumulator = 0
        start_time = time.time()
        insertions = 2
        while idx < len(self.__encoding):
            if(self.__stats != None and it > 0 and it % 50 == 0):
                self.__stats["decompression_rates"].append(decompressing_acumulator/50)
                decompressing_acumulator = 0
            actual_code = self.__encoding[idx : idx+self.__code_size]
            if idx == 0:
                previous_str = self.__table.search(actual_code)
                idx += self.__code_size
                continue
            insertions += 2
            actual_str = self.__table.search(actual_code) 
            if (actual_str != None):# codigo na tabela
                if self.__inserted_strs.search(previous_str + actual_str[0]) == None:
                    code_in_binary = bin(self.__code_count)[2:].zfill(self.__code_size)
                    self.__table.insert(code_in_binary, previous_str + actual_str[0])
                    self.__inserted_strs.insert(previous_str + actual_str[0],0)
                    self.__code_count += 1
                decoding += previous_str
                decompressing_acumulator += len(previous_str)
                previous_str = actual_str
            else:
                code_in_binary = bin(self.__code_count)[2:].zfill(self.__code_size)
                self.__table.insert(code_in_binary,previous_str + previous_str[0])
                self.__inserted_strs.insert(previous_str + previous_str[0],0)
                self.__code_count += 1
                decoding += previous_str
                decompressing_acumulator += len(previous_str)
                previous_str = previous_str + previous_str[0]
    
            idx += self.__code_size
            it += 1
        
        end_time = time.time()
        self.__stats["time"] = end_time - start_time
        self.__stats["dict_size"] = insertions                            
        decoding += previous_str    
        return decoding, self.__stats
    
    
        
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
            
            