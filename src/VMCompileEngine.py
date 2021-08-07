import VMCode as vm
import JackTokenizer as lexer

class VMCompileEngine:
    def __init__(self, fname):
        self.vm = vm.VMCode()
        self.jt = lexer.JackTokenizer(fname)
        
        self.op = ['+', '-', '*', '/', '&', '|', '<', '>', '=']
        self.unaryOp = ['-', '~']

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

    def compileClass(self):
    # compila uma classe completa
        result = ''

        return 0

    def compileClassVarDec(self):
    # compila uma variavel declarada STATIC ou declarada FIELD
        return 0

    def compileSubroutineDec(self):
    # compila um metodo(METHOD), uma função(FUNCTION) ou um construtor(CONSTRUCTOR) completo
        return 0
    
    def compileParameterList(self):
    # compila uma lista de parametros
        return 0

    def compileSubroutineBody(self):
    # compila um corpo de subroutina
        return 0

    def compileVarDec(self):
    # compila uma declaração de variavel
        return 0

    def compileStatements(self):
    # compila uma sequencia de Statements
        return 0

    def compileLet(self):
    # compila um Statement Let
        return 0

    def compileIf(self):
    # compila um Statement If
        return 0

    def compileWhile(self):
    # compila um Statement While
        return 0

    def compileDo(self):
    # compila um Statement Do
        return 0

    def compileReturn(self):
    # compila um Statement Return
        result = self.vm.writeReturn()
        self.nextToken()

        if (self.tokenC != ';'):
            result += self.compileExpression()
        else:
            self.nextToken()

        return result

    def compileExpression(self):
    # compila uma expressão
        result = self.compileTerm()
        self.nextToken()

        while self.tokenC in self.op:
            result = self.compileTerm()
            result += 'op'
            self.nextToken()

        return result

    def compileTerm(self):
        result = ''

        if (self.tokenT == 'integerConstant'):
            result += self.vm.writePush(self.vm.kindOf(self.tokenC), self.vm.indexOf(self.tokenC))
            self.nextToken()
        elif (self.tokenT == 'identifier'):
            id = self.tokenC
            self.nextToken()

            if (self.tokenC == '['):
                result += self.vm.writePush(self.vm.kindOf(id), self.vm.indexOf(id))
                self.nextToken()
                result += self.compileExpression()
                self.nextToken()
            elif (self.tokenC == '(' or self.tokenC == '.'):
                result += self.compileSubroutineDec(id)
            else:
                result += self.vm.writePush(self.vm.kindOf(id), self.vm.indexOf(id))
        elif(self.tokenT == 'symbol'):
            if (self.tokenC == '('):
                self.nextToken()
                result += self.compileExpression()
                self.nextToken()
            elif (self.tokenC == '-' or self.tokenC == '~'):
                result += self.vm.writeArithmetic(self.tokenC)
                self.nextToken()
                result += self.compileTerm()

        return result

    def compileExpressionList(self):
    # compila uma lista de expressão
        if (self.tokenC == ')'):
            return ''
        else:
            result = self.compileExpression()

            if (self.tokenC == ','):
                self.nextToken()
                result += self.compileExpressionList()

            return result

test = VMCompileEngine()
test.compileClass()