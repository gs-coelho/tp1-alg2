

class encoder():
    def __init__(self, input: str) -> None:
        self.__input = input
        self.__trie = {"0": 0, "1": 1}
        self.__codes_count = 2
        
    def encode(self):
        encoding = []
        I = ""
        for i in self.__input:
            if (I + i) in self.__trie:
                I = I + i
            else:
                encoding.append(self.__trie[I])
                self.__trie[I+i] = self.__codes_count
                self.__codes_count += 1
                I = i
        
        encoding.append(self.__trie[I])
        
        return encoding