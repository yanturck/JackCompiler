import JackTokenizer as lexer

class CompilationEngine:
    def __init__(self, fname):
        self.jt = lexer.JackTokenizer(fname)
        self.tokenC = self.jt.getToken()

    def nextToken(self):
        if (self.jt.hasMoreTokens()):
            self.jt.advance()
            self.tokenC = self.jt.getToken()
        else:
            print('Acabou os Tokens!')

    def compile(self):
        self.nextToken()
        self.compileClass()

    def esperado(self, token): # Comparando o Token Esperado com o Corrente
        # try:
        if (self.tokenC == token):
            return self.jt.tokenType
        # except Exception:
        #     ("expected: " + token + " found: " + self.tokenC)
            
    # Cria um novo mecanismo de compilação com a entrada e saída fornecidas. A próxima rotina chamada deve ser compileClass
    def compileClass(self): # Compila uma classe completa
        s = ""
        s += self.tagTerminal('class')
        s += self.esperado('class')
        self.nextToken()
        s += self.jt.tokenType # identificador da classe
        self.nextToken()
        s += self.esperado('{')
        s += self.compileClassVarDec()
        s += self.compileSubRoutine()
        s += self.esperado('}')
        s += self.untagTerminal('class')
        return s

    def compileClassVarDec(): # Compila uma declaração estática ou uma declaração de campo 
        return 0

    def compileSubroutine(): # Compila um método, função ou construtor completo
        return 0

    def compileParameterList(): # Compila uma lista de parâmetros (possivelmente vazia), sem incluir o caractere "()"
        return 0

    def compileVarDec(): # Compila uma declaração var
        return 0

    def compileStatements(): # Compila uma sequência de declarações, sem incluir o delimitador ‘‘ {} ’’
        return 0

    def compileDo(): # Compila uma instrução do
        return 0

    def compileLet(): # Compila uma instrução let
        return 0

    def compileReturn(): # Compila uma instrução return
        return 0

    def compileIf(): # Compila uma instrução if, possivelmente com uma cláusula else à direita
        return 0

    def compileExpression(): # Compila uma expressão
        return 0

    def compileTeam():
        """Compila um termo.
        Essa rotina enfrenta uma pequena dificuldade ao tentar decidir entre algumas das regras alternativas de análise.
        Especificamente, se o token atual for um identificador, a rotina deve distinguir entre uma variável,
        uma entrada de matriz e uma chamada de sub-rotina. Um único token lookahead, que pode ser '' ['', '' ('' ou ''. '',
        É suficiente para distinguir entre as três possibilidades. Qualquer outro token não faz parte deste termo e não deve ser avançado sobre."""
        return 0

    def compileExpressionList(): # Compila uma lista de expressões (possivelmente vazia) separada por vírgulas
        return 0

    def tagTerminal(tag):
        return "<" + tag + ">\n"

    def untagTerminal(tag):
        return "</" + tag + ">\n"