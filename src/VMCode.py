
class VMCode():
    def __init__(self):
        self.tableSymbolClass = [] # tabela de simbolos nivel de classe
        self.tableSymbolSR = [] # tabela de simbolos nivel subroutina
        self.nivelClass = True # apontando o nivel

    # SymbolTable ==================================================
    def startSubRoutine():
    # começa um novo escopo de sub-routina (ou seja, reinicia a tabela de simbolos da subroutina)
        return 0

    def define(name, type, kind, self): # kind = STATIC, FIELD, ARG ou VAR
    # define um novo identificador com o name, type e kind fornecidos e atribui a ele um índice em execução
    # identificadores STATIC e FIELD tem uma escopo de classe, enquanto os identificadores ARG e VAR possuem uma escopo de subroutine
        symbol = {
            'name': name,
            'type': type,
            'kind': kind,
            '#': self.varCount(kind)
        }
        return symbol

    def varCount(kind, self): # kind = STATIC, FIELD, ARG ou VAR
    # retorna o número de variaveis do kind dado já definido no escopo corrente
        count = 0
        
        if (self.nivelClass == True):
            for i in self.tableSymbolClass:
                if (kind == i['kind']):
                    count += 1
        else:
            for i in self.tableSymbolSR:
                if (kind == i['kind']):
                    count += 1

        return count # retorna um inteiro

    def kindOf(name):
    # retorna o kind do nome do identificador no escopo corrente
    # se o identificador é desconhecido no escopo corrente, logo, retorna NONE
        return 0 # retorna um STATIC, FIELD, ARG, VAR ou NONE

    def typeOf(name):
    # retorna um type do nome do identificador no escopo corrente
        return 0 # retorna uma String
    
    def indexOf(name):
    # retorna o indice atribuido para o nome do identificador.
        return 0 # retorna um inteiro

    # VMWriter =====================================================
    def writePush(segment, index): # segment = CONST, ARG, LOCAL, STATIC, THIS, THAT, POINTER, TEMP; index = Int
    # escreve um comando VM push
        return 0

    def writePop(segment, index): # segment = CONST, ARG, LOCAL, STATIC, THIS, THAT, POINTER, TEMP; index = Int
    # escreve um comando VM pop
        return 0

    def writeArithmetic(command): # command = ADD, SUB, NEG, EQ, GT, LT, AND, OR, NOT
    # escreve um comando VM lógico aritmético
        return 0
    
    def writeLabel(label):
    # escreve um comando VM label
        return 0

    def writeGoto(label):
    # escreve um comando VM goto
        return 0
    
    def writeIf(label):
    # escreve um comando VM if-goto
        return 0

    def writeCall(name, nArgs): # name = String, nArgs = Int
    # escreve um comando VM call
        return 0

    def writeFunction(name, nLocals): # name = String, nLocals = Int
    # escreve um comando VM function
        return 0

    def writeReturn():
    # escreve um comando VM return
        return 0

    # def close():
    # # fecha o arquivo de saída
    #     return 0