import JackTokenizer as lexer

class CompilationEngine:
    def __init__(self, fname):
        self.jt = lexer.JackTokenizer(fname)
        self.tokenC = ''
        self.tagToken = ''
        self.tokenT = ''

    def nextToken(self):
        if (self.jt.hasMoreTokens()):
            self.jt.advance()
            self.tokenC = self.jt.getToken()
            self.tokenT = self.jt.tokenType(self.tokenC)
            self.tagToken = self.jt.tagToken(self.tokenC)

    def compile(self):
        self.nextToken()
        return self.compileClass()

    def esperado(self, token): # Comparando o Token Esperado com o Corrente
        if (self.tokenC == token):
            return self.jt.tagToken(token)

    # Estrutura do Programa ========================================================================

    # 'class' className '{' classVarDec* subroutineDec* '}'
    def compileClass(self): # Compila uma classe completa
        result = self.tagTerminal('class')
        result += self.esperado('class')
        self.nextToken()
        result += self.tagToken # identificador da classe
        self.nextToken()
        result += self.esperado('{')
        self.nextToken()
        result += self.compileClassVarDec()
        result += self.compileSubRoutine()
        result += self.esperado('}')
        result += self.untagTerminal('class')
        return result

    # ( 'static' | 'field' ) type varName ( ',' varName)* ';'
    def compileClassVarDec(self): # Compila uma declaração estática(Static) ou uma declaração de campo(Field)
        result = ''
        vars = ['field', 'static']
        
        if self.tokenC in vars:
            result += self.tagTerminal('classVarDec')
            result += self.esperado(self.tokenC)
            self.nextToken()
            result += self.compileType()
            self.nextToken()
            result += self.tagToken # identificador
            self.nextToken()
            result += self.compileListId()
            result += self.untagTerminal('classVarDec')
            self.nextToken()
            result += self.compileClassVarDec()

        return result

    # int' | 'char' | 'boolean' | className
    def compileType(self):
        types = ['int', 'char', 'boolean', 'void']
        if self.tokenC in types:
            return self.esperado(self.tokenC)
        elif (self.tokenT == 'identifier'):
            return self.tagToken

    # ( 'constructor' | 'function' | 'method' ) ( 'void' | type) subroutineName '(' parameterList ')' subroutineBody
    def compileSubRoutine(self): # Compila um método, função ou construtor completo
        result = ''
        subRoutines = ['constructor', 'function', 'method']

        if self.tokenC in subRoutines:
            result += self.tagTerminal('subroutineDec')
            result += self.tagToken
            self.nextToken()
            result += self.compileType()
            self.nextToken()
            result += self.tagToken # identificador
            self.nextToken()
            result += self.esperado('(')
            self.nextToken()
            result += self.tagTerminal('parameterList')
            result += self.compileParameterList()
            result += self.untagTerminal('parameterList')
            result += self.esperado(')')
            self.nextToken()
            result += self.compileSubRoutineBody()
            result += self.untagTerminal('subroutineDec')
            result += self.compileSubRoutine()

        return result

    # ((type varName) ( ',' type varName)*)?
    def compileParameterList(self): # Compila uma lista de parâmetros (possivelmente vazia), sem incluir o caractere "()"
        result = ''

        if (self.tokenC == ','):
            result += self.esperado(',')
            self.nextToken()
            result += self.compileParameterList()
        elif (self.tokenT == 'identifier' or self.tokenT == 'keyword'):
            result += self.compileType()
            self.nextToken()
            result += self.tagToken # identificador
            self.nextToken()
            result += self.compileParameterList()

        return result

    # '{' varDec* statements '}'
    def compileSubRoutineBody(self):
        result = self.tagTerminal('subroutineBody')
        result += self.esperado('{')
        self.nextToken()
        result += self.compileVarDec()
        result += self.compileStatements()
        result += self.esperado('}')
        self.nextToken()
        result += self.untagTerminal('subroutineBody')
        return result

    # 'var' type varName ( ',' varName)* ';'
    def compileVarDec(self): # Compila uma declaração var
        result = ''

        if (self.tokenC == 'var'):
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

    # Statements ========================================================================
    
    # statement*
    def compileStatements(self): # Compila uma sequência de declarações, sem incluir o delimitador ‘‘ {} ’’
        result = self.tagTerminal('statements')
        result += self.compileStatement()
        result += self.untagTerminal('statements')
        return result

    # letStatement | ifStatement | whileStatement | doStatement | returnStatement
    def compileStatement(self): # Compila uma declaração, sem incluir o delimitador ‘‘ {} ’’
        result = ''

        if (self.tokenC == 'let'):
            result += self.compileLetStatement()
            result += self.compileStatement()
        elif (self.tokenC == 'if'):
            result += self.compileIfStatement()
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

    # 'let' varName ( '[' expression ']' )? '=' expression ';'
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

    # 'if' '(' expression ')' '{' statements '}' ( 'else' '{' statements '}' )?
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

    # 'while' '(' expression ')' '{' statements '}'
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

    # 'do' subroutineCall ';'
    def compileDoStatement(self): # Compila uma instrução do
        result = self.tagTerminal('doStatement')
        result += self.esperado('do')
        self.nextToken()
        result += self.compileSubRoutineCall()
        result += self.esperado(';')
        self.nextToken()
        result += self.untagTerminal('doStatement')
        return result

    # 'return' expression? ';'
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

    # Expressions ========================================================================
    
    # term (op term)*
    def compileExpression(self): # Compila uma expressão
        result = self.tagTerminal('expression')
        result += self.compileTerm()
        result += self.compileOp()
        result += self.untagTerminal('expression')
        return result

    # integerConstant | stringConstant | keywordConstant | varName | varName '[' expression ']' | subroutineCall | '(' expression ')' | unaryOp term
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

    # subroutineName '(' expressionList ')' | (className|varName) '.' subroutineName '(' expressionList ')'
    def compileSubRoutineCall(self):
        # result = self.tagTerminal('subroutineCall')
        result = self.tagToken # SubRoutineName
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
            result += self.tagTerminal('expressionList')
            result += self.compileExpressionList()
            result += self.untagTerminal('expressionList')
            result += self.esperado(')')

        self.nextToken()
        # result += self.untagTerminal('subroutineCall')
        return result

    # (expression ( ',' expression)* )?
    def compileExpressionList(self): # Compila uma lista de expressões (possivelmente vazia) separada por vírgulas
        if (self.tokenC == ')'):
            return ''
        else:
            result = self.compileExpression()

            if (self.tokenC == ','):
                result += self.esperado(',')
                self.nextToken()
                result += self.compileExpressionList()

            return result

    # '+' | '-' | '* | '/' | '&' | '|' | '<' | '>' | '='
    def compileOp(self):
        result = ''
        simbolos = ['+', '*', '/', '&', '|', '<', '>', '=']
        
        if self.tokenC in simbolos:
            result += self.tagToken
            self.nextToken()
            result += self.compileTerm()
            result += self.compileOp()

        return result

    # '-' | '~'
    # def compileUnaryOp():

    # 'true | 'false' | 'null' | 'this'
    # def compileKeywordConstant
    
    def tagTerminal(self, tag):
        return '<' + tag + '>\n'
    def untagTerminal(self, tag):
        return '</' + tag + '>\n'