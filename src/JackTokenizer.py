import re

class JackTokenizer:

    def __init__(self, fname):
        self.tokenCorrente = ''
        self.tokens = []
        self.simbolos = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~']
        self.keyWords = ['class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int', 'char',
                    'boolean', 'void', 'true', 'false', 'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return']
        self.prog = fname

        # removendo comentarios
        expReCmt = re.compile(r'//.*\n|/\*(.|\n)*?\*/') # expressão regular para os comentários
        self.prog = expReCmt.sub('', self.prog) # removendo comentarios

        # capturando tokens no programa
        self.tokens = re.findall(r'".*"|[a-zA-Z_]+\w*|\d+|[+|*|/|\-|{|}|(|)|\[|\]|\.|,|;|=|~|>|<|&]', self.prog)

    def hasMoreTokens(self): # verifica e existencia de mais tokens
        if len(self.tokens) != 0:
            return True
        else:
            return False

    def advance(self): # avança para o proximo token
        self.tokenCorrente = self.tokens.pop(0) # atualizando token corrente

    def getToken(self): # retorna o token corrente
        return self.tokenCorrente

    def tokenType(self, token): # retorna o tipo do token corrente
        if token in self.simbolos:
            return 'symbol'
        elif token in self.keyWords:
            return 'keyword'
        elif (token[0] == '"') and (token[-1] == '"'):
            return 'stringConst'
        elif (token.isdigit() == True):
            return 'integerConstant'
        else:
            return 'identifier'

    def tagToken(self, token):
        tokenT = self.tokenType(token)
        if (token == '&'): # substituindo simbolo
            return('<'+tokenT+'> ' + '&amp;' + ' </'+tokenT+'>\n')
        elif (token == '>'): # substituindo simbolo
            return('<'+tokenT+'> ' + '&gt;' + ' </'+tokenT+'>\n')
        elif (token == '<'): # substituindo simbolo
            return('<'+tokenT+'> ' + '&lt;' + ' </'+tokenT+'>\n')
        elif (tokenT == 'stringConst'):
            return('<'+tokenT+'> ' + token[1:len(token)-1] + ' </'+tokenT+'>\n')
        else:
            return('<'+tokenT+'> ' + token + ' </'+tokenT+'>\n')