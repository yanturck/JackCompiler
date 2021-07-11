from re import escape
import JackTokenizer as lexer

class CompilationEngine:
    def __init__(self, fname):
        self.jt = lexer.JackTokenizer(fname)
        self.tokenC = ''
        self.tagToken = ''
        self.tokenT = ''
        self.nextToken()

    def nextToken(self):
        if (self.jt.hasMoreTokens()):
            self.jt.advance()
            self.tokenC = self.jt.getToken()
            self.tokenT = self.jt.tokenType(self.tokenC)
            self.tagToken = self.jt.tagToken(self.tokenC)
        # else:
        #     print('Acabou os Tokens!')

    def compile(self):
        # self.nextToken()
        # self.compileClass()
        return self.compileVarDec()

    def esperado(self, token): # Comparando o Token Esperado com o Corrente
        # try:
        if (self.tokenC == token):
            return self.jt.tagToken(token)
        # except Exception:
        #     ("expected: " + token + " found: " + self.tokenC)
            
    # Cria um novo mecanismo de compilação com a entrada e saída fornecidas. A próxima rotina chamada deve ser compileClass
    def compileClass(self): # Compila uma classe completa
        result = self.tagTerminal('class')
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

        return result

    def compileType(self):
        types = ['int', 'char', 'boolean', 'void']
        if self.tokenC in types:
            return self.esperado(self.tokenC)

    def compileListId(self):
        result = ''

        if (self.tokenT == 'identifier'):
            result += self.tagToken
            self.nextToken()
            result += self.compileListId()
        elif (self.tokenC == ','):
            result += self.esperado(',')
            self.nextToken()
            result += self.compileListId()
        elif (self.tokenC == ';'):
            result += self.esperado(';')

        return result

    def compileVarDec(self): # Compila uma declaração var
        result = ''
        vars = ['field', 'static']
        
        if self.tokenC in vars:
            result += self.tagTerminal('varDec')
            result += self.esperado(self.tokenC)
            self.nextToken()
            result += self.compileType()
            self.nextToken()
            result += self.tagToken # identificador
            self.nextToken()
            result += self.compileListId()
            result += self.untagTerminal('varDec')
            self.nextToken()
            result += self.compileVarDec()

        return result

    def compileSubRoutine(): # Compila um método, função ou construtor completo
        return 0

    def compileSubRoutineCall(self):
        result = self.tagTerminal('subroutineCall')
        result += self.tagToken # SubRoutineName
        self.nextToken()

        if (self.tokenC == '('):
            result += self.esperado('(')
            self.nextToken()
            result += self.tagTerminal('expressionList')
            result += self.compileExpressionList()
            result += self.untagTerminal('expressionList')
            result += self.esperado(')')
        elif (self.tokenC == '.'):
            result += self.esperado('.')
            self.nextToken()
            result += self.tagToken # SubRoutineName
            self.nextToken()
            result += self.esperado('(')
            self.nextToken()
            result += self.compileExpressionList()
            result += self.esperado(')')

        self.nextToken()
        result += self.untagTerminal('subroutineCall')
        return result

    def compileParameterList(): # Compila uma lista de parâmetros (possivelmente vazia), sem incluir o caractere "()"
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
            result += self.compileWhileStatement()
            result += self.compileStatement()
        elif (self.tokenC == 'do'):
            result += self.compileDoStatement()
            result += self.compileStatement()
        elif (self.tokenC == 'return'):
            result += self.compileReturnStatement()
            result += self.compileStatement()

        return result

    def compileStatements(self): # Compila uma sequência de declarações, sem incluir o delimitador ‘‘ {} ’’
        result = self.tagTerminal('statements')
        result += self.compileStatement()
        result += self.untagTerminal('statements')
        return result

    def compileDoStatement(self): # Compila uma instrução do
        result = self.tagTerminal('doStatement')
        result += self.esperado('do')
        self.nextToken()
        result += self.compileSubRoutine()
        result += self.esperado(';')
        self.nextToken()
        result += self.untagTerminal('doStatement')
        return 0

    def compileLetStatement(self): # Compila uma instrução let
        result = self.tagTerminal('letStatement')
        result += self.esperado('let')
        self.nextToken()
        result += self.tagToken # identificador
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

    def compileReturnStatement(self): # Compila uma instrução return
        result = self.tagTerminal('returnStatement')
        result += self.esperado('return')
        self.nextToken()

        if (self.tokenC != ';'):
            result += self.compileExpression()

        result += self.esperado(';')
        self.nextToken()
        result += self.untagTerminal('returnStatement')
        return result

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

    def compileWhileStatement(self):
        result = self.tagTerminal('whileStatement')
        result += self.esperado('while')
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
        result += self.untagTerminal('whileStatement')
        return result

    def compileExpression(self): # Compila uma expressão
        result = self.tagTerminal('expression')
        result += self.compileTerm()
        result += self.compileOp()
        result += self.untagTerminal('expression')
        return result

    def compileTerm(self):
        """Compila um termo.
        Essa rotina enfrenta uma pequena dificuldade ao tentar decidir entre algumas das regras alternativas de análise.
        Especificamente, se o token atual for um identificador, a rotina deve distinguir entre uma variável,
        uma entrada de matriz e uma chamada de sub-rotina. Um único token lookahead, que pode ser '' ['', '' ('' ou ''. '',
        É suficiente para distinguir entre as três possibilidades. Qualquer outro token não faz parte deste termo e não deve ser avançado sobre."""
        result = self.tagTerminal('term')
        
        if (self.tokenT == 'integerConstant' or self.tokenT == 'stringConst' or self.tokenT == 'keyword'):
            result += self.tagToken
            self.nextToken()
        elif (self.tokenT == 'identifier'):
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
        elif (self.tokenT == 'symbol'):
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

    def compileOp(self):
        result = ''
        simbolos = ['+', '*', '/', '&', '|', '<', '>', '=']
        
        if self.tokenC in simbolos:
            result += self.tagToken
            self.nextToken()
            result += self.compileTerm()
            result += self.compileOp()

        return result

    def compileExpressionList(self): # Compila uma lista de expressões (possivelmente vazia) separada por vírgulas
        result = self.compileExpression()

        if (self.tokenC == ','):
            result += self.esperado(',')
            self.nextToken()
            result += self.compileExpressionList()

        return result

    
    def tagTerminal(self, tag):
        return '<' + tag + '>\n'
    def untagTerminal(self, tag):
        return '</' + tag + '>\n'

cp = CompilationEngine('// Location on the screen\nfield int x, y;\n// The size of the square\nfield int size;\\static boolean v, f;')
print(cp.compile())