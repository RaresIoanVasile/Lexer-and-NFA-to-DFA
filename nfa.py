import copy
from collections import OrderedDict

class NFA:
    def __init__(self, string):
        self.alphabet = {string}
        self.number_of_states = 2
        self.initial_state = 0
        self.final_state = 1
        self.delta_func = {}
        self.delta_func[(0, string)] = [1]

    def __str__(self):
        return str(self.alphabet) + "\n" + str(self.number_of_states) + "\n" + str(self.initial_state) + "\n" + str(self.final_state) + "\n" + str(self.delta_func)

class NFA_Star:
    def __init__(self, nfa):
        self.alphabet = nfa.alphabet
        self.number_of_states = nfa.number_of_states + 2
        self.initial_state = 0
        self.final_state = nfa.final_state + 2
        self.delta_func = {}
        self.delta_func[(self.initial_state, '')] = [nfa.initial_state + 1, self.final_state]
        self.delta_func[(nfa.final_state + 1, '')] = [nfa.initial_state + 1, self.final_state]
        nfa_copy = copy.deepcopy(nfa)
        for key, value in nfa_copy.delta_func.items():
            for i in range(0, len(value)):
                value[i] = value[i] + 1
            self.delta_func[(key[0] + 1, key[1])] = value
        
    def __str__(self):
        return str(self.alphabet) + "\n" + str(self.number_of_states) + "\n" + str(self.initial_state) + "\n" + str(self.final_state) + "\n" + str(self.delta_func)

class NFA_Concat:
    def __init__(self, nfa1, nfa2):
        self.alphabet = set.union(nfa1.alphabet, nfa2.alphabet)
        self.number_of_states = nfa1.number_of_states + nfa2.number_of_states - 1
        self.initial_state = nfa1.initial_state
        self.final_state = self.number_of_states - 1
        self.delta_func = {}
        nfa_copy = copy.deepcopy(nfa2)
        for key, value in nfa_copy.delta_func.items():
            for i in range(0, len(value)):
                value[i] = value[i] + nfa1.final_state
            self.delta_func[(key[0] + nfa1.final_state, key[1])] = value
        nfa_copy = copy.deepcopy(nfa1)
        for key, value in nfa_copy.delta_func.items():
            self.delta_func[key] = value
        
    def __str__(self):
        return str(self.alphabet) + "\n" + str(self.number_of_states) + "\n" + str(self.initial_state) + "\n" + str(self.final_state) + "\n" + str(self.delta_func)

class NFA_Union:
    def __init__(self, nfa1, nfa2):
        self.alphabet = set.union(nfa1.alphabet, nfa2.alphabet)
        self.number_of_states = nfa1.number_of_states + nfa2.number_of_states  + 2
        self.initial_state = 0
        self.final_state = self.number_of_states - 1
        self.delta_func = {}
        self.delta_func[(self.initial_state, '')] = [nfa1.initial_state + 1, nfa2.initial_state + nfa1.final_state + 2]
        self.delta_func[(nfa1.final_state + 1, '')] = [self.final_state]
        self.delta_func[(nfa2.final_state + nfa1.final_state + 2, '')] = [self.final_state]
        nfa_copy = copy.deepcopy(nfa1)
        for key, value in nfa_copy.delta_func.items():
            for i in range(0, len(value)):
                value[i] = value[i] + 1
            self.delta_func[key[0] + 1, key[1]] = value
        nfa_copy = copy.deepcopy(nfa2)
        for key, value in nfa_copy.delta_func.items():
            for i in range(0, len(value)):
                value[i] = value[i] + nfa1.final_state + 2
            self.delta_func[key[0] + nfa1.final_state + 2, key[1]] = value

    def __str__(self):
        return str(self.alphabet) + "\n" + str(self.number_of_states) + "\n" + str(self.initial_state) + "\n" + str(self.final_state) + "\n" + str(self.delta_func)

class op:
    def parse(string):
        stack = []
        aux = string.split(' ')
        aux = aux[::-1]
        for i in range(0, len(aux)):
            if aux[i] == 'STAR':
                stack.append(NFA_Star(stack.pop()))
            elif aux[i] == 'PLUS':
                nfa_aux = copy.deepcopy(stack.pop())
                stack.append(NFA_Concat(nfa_aux, NFA_Star(nfa_aux)))
            elif aux[i] == 'CONCAT':
                stack.append(NFA_Concat(stack.pop(), stack.pop()))
            elif aux[i] == 'UNION':
                stack.append(NFA_Union(stack.pop(), stack.pop()))
            else:
                stack.append(NFA(aux[i]))   
        return stack.pop()

    def NFA_to_DFA(nfa, out_file):
        print(nfa.delta_func)
        outt = open(out_file, "w")
        if (0,'') in nfa.delta_func:
            initial_state = []
            initial_state.append(0)
            initial_state.sort()
            for i in initial_state:
                if (i,'') in nfa.delta_func:
                    for x in nfa.delta_func[(i, '')]:
                        if x not in initial_state:
                            initial_state.append(x)
                else:
                    continue
            initial_state.sort()
        else:
            initial_state = [0]
        initial_state = list(set(initial_state))
        new_states = [initial_state] 

        for state in new_states:
            for litera in nfa.alphabet:
                for i in state:
                    if (i, litera) in nfa.delta_func:
                        lista = nfa.delta_func[(i, litera)]
                        for j in lista:
                            if (j, '') in nfa.delta_func:
                                for x in nfa.delta_func[(j, '')]:
                                    if x not in lista:
                                        lista.append(x)
                        lista = list(set(lista))
                        lista.sort()
                        if lista not in new_states:
                            new_states.append(lista)
        print(new_states)
        transitions = []
        for state in new_states:
            for litera in nfa.alphabet:
                for i in state:
                    if (i, litera) in nfa.delta_func:
                        aux = list(set(nfa.delta_func[(i, litera)]))
                        aux.sort()
                        transitions.append(((new_states.index(state), litera), new_states.index(aux)))
                    else:
                        transitions.append(((new_states.index(state), litera), len(new_states)))
        for litera in nfa.alphabet:
            transitions.append(((len(new_states), litera), len(new_states)))
        transitions = list(set(transitions))
        transitions.sort()
        transitions_bun = []
        print(transitions)
        i = 0
        while i < len(transitions) - 1:
            if transitions[i][0] == transitions[i+1][0] and transitions[i][0] == transitions[i+2][0]:
                transitions_bun.append(transitions[i+1])
                i = i + 3
            elif transitions[i][0] == transitions[i+1][0]:
                transitions_bun.append(transitions[i])
                i = i + 2
            else:
                transitions_bun.append(transitions[i])
                i = i + 1

        transitions_bun.append(transitions[len(transitions) - 1])
        print(transitions_bun)
        alphabet = list(nfa.alphabet)
        aux = ''.join(alphabet)
        outt.write(aux)
        outt.write("\n")
        number_of_states = len(new_states) + 1
        outt.write(str(number_of_states))
        outt.write("\n")
        initial_state = 0
        outt.write(str(initial_state))
        outt.write("\n")
        final_states = []
        for state in new_states:
            for i in state:
                if i == nfa.final_state:
                    final_states.append(new_states.index(state))
        final_states = list(set(final_states))
        aux = ''
        for i in final_states:
            aux = aux + str(i) + ' '
        aux = aux[:-1]
        outt.write(aux)
        outt.write("\n")
        for i in transitions_bun:
            outt.write(str(i[0][0]) + ",'" + str(i[0][1]) + "'," + str(i[1]))
            if transitions_bun.index(i) != (len(transitions_bun) - 1):
                outt.write("\n")

        outt.close()

