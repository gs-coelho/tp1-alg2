
class decoder():
    def __init__(self, encoding) -> None:
        self.__encoding = encoding
        self.__table = ["0","1"]
        
    def decode(self):
        decoding = ""
        previous_str = ""
        for idx, actual_code in enumerate(self.__encoding):
            if idx == 0:
                previous_str = self.__table[actual_code]
                continue
            if (0 <= actual_code < len(self.__table)):# codigo na tabela
                if (previous_str + self.__table[actual_code][0]) not in self.__table:
                    self.__table.append(previous_str + self.__table[actual_code][0])
                decoding += previous_str
                previous_str = self.__table[actual_code]
            else:
                self.__table.append(previous_str + previous_str[0])
                decoding += previous_str
                previous_str = previous_str + previous_str[0]
            
            
        decoding += previous_str    
        return decoding