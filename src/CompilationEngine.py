from re import escape
import JackTokenizer as lexer

class CompilationEngine:
    def __init__(self, fname):
        self.jt = lexer.JackTokenizer(fname)
        self.tokenC = self.jt.getToken()
        self.nextToken()
        self.tagToken = self.jt.tagToken(self.tokenC)

    def nextToken(self):
        if (self.jt.hasMoreTokens()):
            self.jt.advance()
            self.tokenC = self.jt.getToken()
            self.tagToken = self.jt.tagToken(self.tokenC)
        # else:
        #     print('Acabou os Tokens!')

    def compile(self):
        # self.nextToken()
        # self.compileClass()
        return self.compileIfStatement()

    def esperado(self, token): # Comparando o Token Esperado com o Corrente
        # try:
        if (self.tokenC == token):
            return self.jt.tagToken(token)
        # except Exception:
        #     ("expected: " + token + " found: " + self.tokenC)
            
    # Cria um novo mecanismo de compilação com a entrada e saída fornecidas. A próxima rotina chamada deve ser compileClass
    def compileClass(self): # Compila uma classe completa
        result = ""
        result += self.tagTerminal('class')
        result += self.esperado('class')
        self.nextToken()
        result += self.jt.tokenType # identificador da classe
        self.nextToken()
        result += self.esperado('{')
        result += self.compileClassVarDec()
        result += self.compileSubRoutine()
        result += self.esperado('}')
        result += self.untagTerminal('class')
        return result

    def compileClassVarDec(self): # Compila uma declaração estática(Static) ou uma declaração de campo(Field)
        result = ""
        return 0

    def compileSubRoutine(): # Compila um método, função ou construtor completo
        return 0

    def compileParameterList(): # Compila uma lista de parâmetros (possivelmente vazia), sem incluir o caractere "()"
        return 0

    def compileVarDec(): # Compila uma declaração var
        return 0

    def compileStatement(self): # Compila uma declaração, sem incluir o delimitador ‘‘ {} ’’
        result = ''

        if (self.tokenC == 'let'):
            result += self.compileLetStatement()
            result += self.compileStatement()
        elif (self.tokenC == 'if'):
            result += self.compileIftStatement()
            result += self.compileStatement()
        elif (self.tokenC == 'while'):
            result += self.compileWhiletStatement()
            result += self.compileStatement()
        elif (self.tokenC == 'do'):
            result += self.compileDotStatement()
            result += self.compileStatement()
        elif (self.tokenC == 'return'):
            result += self.compileReturntStatement()
            result += self.compileStatement()

        return result

    def compileStatements(self): # Compila uma sequência de declarações, sem incluir o delimitador ‘‘ {} ’’
        result = self.tagTerminal('statements')
        result += self.compileStatement()
        result += self.untagTerminal('statements')
        return result

    def compileDo(self): # Compila uma instrução do
        result = ""
        result += self.esperado('do')
        self.nextToken()

        return 0

    def compileLetStatement(self): # Compila uma instrução let
        result = self.tagTerminal('letStatement')
        result += self.esperado('let')
        self.nextToken()
        result += self.tagToken
        self.nextToken()

        if (self.tokenC == '['):
            result += self.esperado('[')
            self.nextToken()
            result += self.compileExpression()
            result += self.esperado(']')
            self.nextToken()

        result += self.esperado('=')
        self.nextToken()
        result += self.compileExpression()
        result += self.esperado(';')
        self.nextToken()
        result += self.untagTerminal('letStatement')
        return result

    def compileReturn(): # Compila uma instrução return
        return 0

    def compileIfStatement(self): # Compila uma instrução if, possivelmente com uma cláusula else à direita
        result = self.tagTerminal('ifStatement')
        result += self.esperado('if')
        self.nextToken()
        result += self.esperado('(')
        self.nextToken()
        result += self.compileExpression()
        result += self.esperado(')')
        self.nextToken()
        result += self.esperado('{')
        self.nextToken()
        result += self.compileStatements()
        result += self.esperado('}')
        self.nextToken()

        if (self.tokenC == 'else'):
            result += self.esperado('else')
            self.nextToken()
            result += self.esperado('{')
            self.nextToken()
            result += self.compileStatements()
            result += self.esperado('}')
            self.nextToken()

        result += self.untagTerminal('ifStatement')
        return result

    def compileExpression(self): # Compila uma expressão
        result = self.tagTerminal('expression')
        result += self.compileTerm()
        result += self.compileSubTerms()
        result += self.untagTerminal('expression')
        return result

    def compileTerm(self):
        """Compila um termo.
        Essa rotina enfrenta uma pequena dificuldade ao tentar decidir entre algumas das regras alternativas de análise.
        Especificamente, se o token atual for um identificador, a rotina deve distinguir entre uma variável,
        uma entrada de matriz e uma chamada de sub-rotina. Um único token lookahead, que pode ser '' ['', '' ('' ou ''. '',
        É suficiente para distinguir entre as três possibilidades. Qualquer outro token não faz parte deste termo e não deve ser avançado sobre."""
        result = self.tagTerminal('term')
        
        tokenT = self.jt.tokenType(self.tokenC)
        if (tokenT == 'integerConstant' or tokenT == 'stringConst' or tokenT == 'keyword'):
            result += self.tagToken
            self.nextToken()
        elif (tokenT == 'identifier'):
            id = self.tokenC
            self.nextToken()
            
            if (self.tokenC == '['):
                result += self.jt.tagToken(id)
                result += self.esperado('[')
                self.nextToken()
                result += self.compileExpression()
                result += self.esperado(']')
                self.nextToken()
            elif (self.tokenC == '(' or self.tokenC == '.'):
                result += self.compileSubRoutine(id)
            else:
                result += self.jt.tagToken(id)
        elif (tokenT == 'symbol'):
            if (self.tokenC == '('):
                result += self.tagToken
                self.nextToken()
                result += self.compileExpression()
                result += self.esperado(')')
                self.nextToken()
            elif (self.tokenC == '-' or self.tokenC == '~'):
                result += self.tagToken
                self.nextToken()
                result += self.compileTerm()
        
        result += self.untagTerminal('term')
        return result

    def compileSubTerms(self):
        result = ''
        simbolos = ['+', '*', '/', '&', '|', '<', '>', '=']
        
        if self.tokenC in simbolos:
            result += self.tagToken
            self.nextToken()
            result += self.compileTerm()
            result += self.compileSubTerms()

        return result

    def compileExpressionList(): # Compila uma lista de expressões (possivelmente vazia) separada por vírgulas
        return 0

    
    def tagTerminal(self, tag):
        return "<" + tag + ">\n"
    def untagTerminal(self, tag):
        return "</" + tag + ">\n"

cp = CompilationEngine('if (x < 0) {\nlet sign = "negative";\n}')
print(cp.compile())