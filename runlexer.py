from typing import Dict

class DFA:
    def __init__(self, string):
        strr = string.split('\n')
        self.alphabet = strr[0]
        self.name = strr[1]
        strr = strr[2:]
        self.initial_state = int(strr[0])
        self.final_states = strr[len(strr) - 1]
        strr = strr[0:len(strr) - 1]
        self.final_states = self.final_states.split(' ')
        self.delta_func = {}
        strr = strr[1:]
        for i in range(0, len(strr)):
            strr[i] = ''.join(map(str, strr[i])).split(',')
        for i in range(0, len(strr)):
            strr[i][1] = strr[i][1].replace("'", '')
            if strr[i][1] == "\\n":
                strr[i][1] = '\n'
            self.delta_func[(int(strr[i][0]), strr[i][1])] = int(strr[i][2])


    def next_config(self, config):
        if (config[0], config[1][0]) in self.delta_func:
            return (self.delta_func[(config[0], config[1][0])], config[1][1:])
        else:
            return 0

    def accept(self, word):
        config = (self.initial_state, word)
        while(len(word) != 0):
            word = word[1:]
            if self.next_config(config) == 0:
                return False
            config = self.next_config(config)
        for i in range(0, len(self.final_states)):
            if config[0] == int(self.final_states[i]):
                return True
        return False

class Lexer:
    def __init__(self, dfa_list):
        self.dfa_list = dfa_list

    def longest_prefix(self, word):
        initial_configs = [0] * len(self.dfa_list)
        words = [0] * len(self.dfa_list)
        for i in range(0, len(words)):
            words[i] = word
        for i in range(0, len(self.dfa_list)):
            initial_configs[i] = (self.dfa_list[i].initial_state, word)
            last_index = [0] * len(self.dfa_list)
        for i in range(0, len(last_index)):
            last_index[i] = 0
        for i in range(0, len(initial_configs)):
            for j in range(1, len(words[i]) + 1):
                if self.dfa_list[i].next_config(initial_configs[i]) == 0:
                    break
                if self.dfa_list[i].accept(words[i][0:j]): 
                    last_index[i] = j
                initial_configs[i] = self.dfa_list[i].next_config(initial_configs[i])

        maxim = max(last_index)
        index = last_index.index(maxim)                
        return (self.dfa_list[index].name, maxim)

    def parse(self, word):
        answear = ''
        while(len(word) != 0):
            if word[0:self.longest_prefix(word)[1]] == '\n':
                answear += self.longest_prefix(word)[0] + " " + "\\n"
            else:
                answear += self.longest_prefix(word)[0] + " " + word[0:self.longest_prefix(word)[1]]
            answear += "\n"
            word = word[self.longest_prefix(word)[1]:]    
        return answear
