
class VMCode():
    def __init__(self):
        self.tableSymbolClass = [] # tabela de simbolos nivel de classe
        self.tableSymbolSR = [] # tabela de simbolos nivel subroutina
        self.nivel = True # aponta o nivel (True = Nivel de Classe e Flase = Nivel de SubRoutine)

    # SymbolTable ==================================================
    def startSubRoutine(self):
    # começa um novo escopo de sub-routina (ou seja, reinicia a tabela de simbolos da subroutina)
        self.nivel = False
        self.tableSymbolSR = []

    def define(self, name, type, kind): # kind = STATIC, FIELD, ARG ou VAR
    # define um novo identificador com o name, type e kind fornecidos e atribui a ele um índice em execução
    # identificadores STATIC e FIELD tem uma escopo de classe, enquanto os identificadores ARG e VAR possuem uma escopo de subroutine
        symbol = {
            'name': name,
            'type': type,
            'kind': kind,
            'index': self.varCount(kind)
        }
        return symbol

    def varCount(self, kind): # kind = STATIC, FIELD, ARG ou VAR
    # retorna o número de variaveis do kind dado já definido no escopo corrente
        count = 0
        
        if (self.nivel == True): # nivel de classe
            for i in self.tableSymbolClass:
                if (kind == i['kind']):
                    count += 1
        else: # nivel de subroutine
            for i in self.tableSymbolSR:
                if (kind == i['kind']):
                    count += 1

        return count # retorna um inteiro

    def kindOf(self, name):
    # retorna o kind do nome do identificador no escopo corrente
    # se o identificador é desconhecido no escopo corrente, logo, retorna NONE
        kind = None

        if (self.nivel == True): # nivel de classe
            for i in self.tableSymbolClass:
                if (name == i['name']):
                    kind = i['kind']
        else: # nivel de subroutine
            for i in self.tableSymbolSR:
                if (name == i['name']):
                    kind = i['kind']

        return kind # retorna um STATIC, FIELD, ARG, VAR ou NONE

    def typeOf(self, name):
    # retorna um type do nome do identificador no escopo corrente
        tipo = None

        if (self.nivel == True): # nivel de classe
            for i in self.tableSymbolClass:
                if (name == i['name']):
                    tipo = i['type']
        else: # nivel de subroutine
            for i in self.tableSymbolSR:
                if (name == i['name']):
                    tipo = i['type']

        return tipo # retorna uma String
    
    def indexOf(self, name):
    # retorna o indice atribuido para o nome do identificador.
        ind = None

        if (self.nivel == True): # nivel de classe
            for i in self.tableSymbolClass:
                if (name == i['name']):
                    ind = i['index']
        else: # nivel de subroutine
            for i in self.tableSymbolSR:
                if (name == i['name']):
                    ind = i['index']

        return ind # retorna um inteiro

    # VMWriter =====================================================
    def writePush(self, segment, index): # segment = CONST, ARG, LOCAL, STATIC, THIS, THAT, POINTER, TEMP; index = Int
    # escreve um comando VM push
        result = 'push' + segment + index
        return result

    def writePop(self, segment, index): # segment = CONST, ARG, LOCAL, STATIC, THIS, THAT, POINTER, TEMP; index = Int
    # escreve um comando VM pop
        result = 'pop' + segment + index
        return result

    def writeArithmetic(self, command): # command = ADD, SUB, NEG, EQ, GT, LT, AND, OR, NOT
    # escreve um comando VM lógico aritmético
        result = None

        if (command == '+'):
            result = 'add'
        elif (command == '-'):
            result = 'sub'
        elif (command == '~'): # ainda não sei
            result = 'neg'
        elif (command == '=='):
            result = 'eq'
        elif (command == '>'):
            result = 'gt'
        elif (command == '<'):
            result = 'lt'
        elif (command == '&'):
            result = 'and'
        elif (command == '|'):
            result = 'or'
        elif (command == '!'):
            result = 'not'
        
        return result
    
    def writeLabel(self, label):
    # escreve um comando VM label
        return 'label ' + label

    def writeGoto(self, label):
    # escreve um comando VM goto
        return 'goto ' + label
    
    def writeIf(self, label):
    # escreve um comando VM if-goto
        return 'if-goto ' + label

    def writeCall(self, name, nArgs): # name = String, nArgs = Int
    # escreve um comando VM call
        return 'call ' + name + str(nArgs)

    def writeFunction(self, name, nLocals): # name = String, nLocals = Int
    # escreve um comando VM function
        return 'function ' + name + str(nLocals)

    def writeReturn(self):
    # escreve um comando VM return
        return 'return'

    # def close():
    # # fecha o arquivo de saída
    #     return 0