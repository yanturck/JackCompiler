import re

class JackTokenizer:

    def __init__(self, fname):
        self.tokenCorrente = ''
        self.tokens = []
        self.simbolos = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&amp;', '|', '&lt;', '&gt;', '=', '~']
        self.keyWords = ['class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int', 'char',
                    'boolean', 'void', 'true', 'false', 'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return']
        self.prog = fname

        # removendo comentarios
        expReCmt = re.compile(r'//.*\n|/\*(.|\n)*?\*/') # expressão regular para os comentários
        self.prog = expReCmt.sub('', self.prog) # removendo comentarios

        # substituindo simbolos <, >, ", e & para nao conflitar com o XML
        ocorEcom = re.compile(r'&')
        self.prog = ocorEcom.sub('&amp;', self.prog) # substituindo
        ocorMaiorQ = re.compile(r'>')
        self.prog = ocorMaiorQ.sub('&gt;', self.prog) # substituindo
        ocorMenorQ = re.compile(r'<')
        self.prog = ocorMenorQ.sub('&lt;', self.prog) # substituindo

        # capturando tokens no programa
        self.tokens = re.findall(r'".*"|[a-zA-Z_]+\w*|\d+|[+|*|/|\-|{|}|(|)|\[|\]|\.|,|;|=|~]|&lt;|&gt;|&amp;', self.prog)

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
            self.tokenCorrente = token[1:len(token)-1]
            return 'stringConst'
        elif (token.isdigit() == True):
            return 'integerConstant'
        else:
            return 'identifier'