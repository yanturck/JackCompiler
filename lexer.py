
class JackTokenizer:
    palavrasChaves = ['class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int', 'char',
                    'boolean', 'void', 'true', 'false', 'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return']

    simbolos = ['{', '}', '(', ')', '[', ']', '. ', ', ', '; ', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~']

    def __init__(self, fname):
        self.prog = fname

    def advance(): # avança para o proximo token
        return 0

    def hasMoreTokens(): # verifica e existencia de mais tokens
        return 0

    def tokenType(): # retorna o tipo do token corrente
        return 0

    def getToken(): # retorna o token corrente
        return 0

    