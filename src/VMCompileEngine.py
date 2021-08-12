from typing import TextIO
import VMCode as vm
import JackTokenizer as lexer

class VMCompileEngine:
    def __init__(self, fname):
        self.vm = vm.VMCode()
        self.jt = lexer.JackTokenizer(fname)
        
        self.op = ['+', '-', '*', '/', '&', '|', '<', '>', '=']
        self.unaryOp = ['-', '~']

        self.tokenC = ''
        self.tokenT = ''
        self.className = ''
        self.auxClassName = ''

        self.countArg = 0
        self.countMethod = 0


    def nextToken(self):
        if (self.jt.hasMoreTokens()):
            self.jt.advance()
            self.tokenC = self.jt.getToken()
            self.tokenT = self.jt.tokenType(self.tokenC)
    
    def esperado(self, token):
        if (self.tokenC == token):
            pass
        else:
            raise Exception('Valor Inesperado')

    def compile(self):
        self.nextToken()
        return self.compileClass()

    def compileClass(self):
    # compila uma classe completa
        self.esperado('class')
        self.nextToken() # tokenC = identificador da classe
        self.className = self.tokenC
        self.nextToken()
        self.esperado('{')
        self.nextToken()
        self.vm.nivel = True # nivel de classe
        self.compileClassVarDec()
        self.vm.nivel = False # Nivel de SubRoutine
        result = self.compileSubroutineDec()
        self.esperado('}')
        return result

    def compileClassVarDec(self):
    # compila uma variavel declarada STATIC ou declarada FIELD
        vars = ['field', 'static']
        
        if self.tokenC in vars:
            kind = self.tokenC
            self.nextToken()
            tipo = self.tokenC # type
            self.nextToken()
            name = self.tokenC # identificador
            self.nextToken()
            self.vm.define(name, tipo, kind)

            while (self.tokenC == ','):
                self.nextToken()
                name = self.tokenC # identificador
                self.nextToken()
                self.vm.define(name, tipo, kind)
            
            self.esperado(';')
            self.nextToken()
            self.compileClassVarDec()

    def compileSubroutineDec(self):
    # compila um metodo(METHOD), uma função(FUNCTION) ou um construtor(CONSTRUCTOR) completo
        result = ''
        subRoutines = ['constructor', 'function', 'method']

        if self.tokenC in subRoutines:
            self.vm.startSubRoutine()
            # tokenC = subRoutines
            subRoutine = self.tokenC
            self.nextToken() # tokenC = tipo
            self.nextToken()
            result += 'function ' + self.className + '.' + self.tokenC + ' ' + str(self.countMethod) + '\n'
            self.nextToken()
            self.esperado('(')
            self.nextToken()
            self.compileParameterList()
            self.esperado(')')
            self.nextToken()

            if (subRoutine == 'constructor'):
                count = len(self.vm.tableSymbolSR)
                result += self.vm.writePush('constant', count)
                result += self.vm.writeCall('Memory.alloc', count-1)
                result += self.vm.writePop('pointer', 0)

            result += self.compileSubroutineBody()
            self.countMethod += 1
            result += self.compileSubroutineDec()
            
        return result
    
    def compileParameterList(self):
    # compila uma lista de parametros
        types = ['int', 'char', 'boolean', 'void']

        if (self.tokenC == ','):
            self.nextToken()
            self.compileParameterList()
        elif(self.tokenC in types):
            tipo = self.tokenC
            self.nextToken()
            name = self.tokenC
            self.vm.define(name, tipo, 'argument')
            self.nextToken()
            self.compileParameterList()

    def compileSubroutineBody(self):
    # compila um corpo de subroutina
        self.esperado('{')
        self.nextToken()
        self.compileVarDec()
        result = self.compileStatements()
        self.esperado('}')
        self.nextToken()
        return result

    def compileVarDec(self):
    # compila uma declaração de variavel
        if (self.tokenC == 'var'):
            self.nextToken()
            tipo = self.tokenC # type
            self.nextToken()
            name = self.tokenC # identificador
            self.nextToken()
            self.vm.define(name, tipo, 'local')

            while (self.tokenC == ','):
                self.nextToken()
                name = self.tokenC # identificador
                self.nextToken()
                self.vm.define(name, tipo, 'local')
            
            self.esperado(';')
            self.nextToken()
            self.compileVarDec()

    def compileStatements(self):
    # compila uma sequencia de Statements
        result = ''

        if (self.tokenC == 'let'):
            result += self.compileLet()
            result += self.compileStatements()
        elif (self.tokenC == 'if'):
            result += self.compileIf()
            result += self.compileStatements()
        elif (self.tokenC == 'while'):
            result += self.compileWhile()
            result += self.compileStatements()
        elif (self.tokenC == 'do'):
            result += self.compileDo()
            result += self.compileStatements()
        elif (self.tokenC == 'return'):
            result += self.compileReturn()
            result += self.compileStatements()

        return result

    def compileLet(self):
    # compila um Statement Let
        result = ''

        self.nextToken() # tokenC = identificador
        id = self.tokenC
        self.nextToken()

        if (self.tokenC == '['):
            self.nextToken()
            result += self.compileExpression()
            self.esperado(']') # tokenC = ]
            self.nextToken()

        self.esperado('=') # tokenC = =
        self.nextToken()
        result += self.compileExpression()
        # print(result)
        # print(self.tokenC)
        self.esperado(';') # tokenC = ;
        self.nextToken()

        result += self.vm.writePop(self.vm.kindOf(id), self.vm.indexOf(id))
        
        return result

    def compileIf(self):
    # compila um Statement If
        result = ''
        self.nextToken()

        label1 = 'IF_TRUE'
        label2 = 'IF_FALSE'
        label3 = 'IF_END'

        self.esperado('(')
        self.nextToken()
        result += self.compileExpression()
        self.esperado(')')
        self.nextToken()
        
        result += self.vm.writeIf(label1) # if-goto L1
        result += self.vm.writeGoto(label2) # goto L2
        result += self.vm.writeLabel(label1) # L1

        self.esperado('{')
        self.nextToken()
        result += self.compileStatements()
        self.esperado('}')
        self.nextToken()
        
        result += self.vm.writeGoto(label3) # goto END
        result += self.vm.writeLabel(label2) # L2

        self.esperado('else')
        self.nextToken()
        self.esperado('{')
        self.nextToken()
        result += self.compileStatements()
        self.esperado('}')
        self.nextToken()

        result += self.vm.writeLabel(label2) # L END

        return result

    def compileWhile(self):
    # compila um Statement While
        result = ''

        label1 = 'WHILE_EXP'
        label2 = 'WHILE_END'

        result += self.vm.writeLabel(label1) # L WHILE EXP

        self.nextToken()
        self.esperado('(')
        self.nextToken()
        result += self.compileExpression()
        self.esperado(')')

        result += self.vm.writeArithmetic('!')
        result += self.vm.writeIf(label2) # if-goto WHILE END

        self.nextToken()
        self.esperado('{')
        self.nextToken()
        result += self.compileStatements()
        self.esperado('}')
        self.nextToken()

        result += self.vm.writeGoto(label1) # goto WHILE EXP
        result += self.vm.writeLabel(label2) # L WHILE END

        return result

    def compileDo(self):
    # compila um Statement Do
        result = ''
        self.nextToken()
        # result += self.compileSubRoutineCall()
        result += self.esperado(';')
        self.nextToken()
        
        return result

    def compileReturn(self):
    # compila um Statement Return
        result = ''
        self.nextToken()

        if (self.tokenC != ';'):
            result += self.compileExpression()
        else:
            self.nextToken()
        
        result += self.vm.writeReturn()
        self.nextToken()
        return result

    def compileExpression(self):
    # compila uma expressão
        result = self.compileTerm()

        while self.tokenC in self.op:
            op = self.tokenC
            self.nextToken()
            result += self.compileTerm()

            if (op == '*'):
                result += self.vm.writeCall('Marh.multiply', 2)
            else:
                result += self.vm.writeArithmetic(op)

        return result

    def compileTerm(self):
        result = ''

        if (self.tokenT == 'integerConstant'):
            result += self.vm.writePush('constant', self.tokenC)
            self.nextToken()
        elif (self.tokenT == 'identifier'):
            id = self.tokenC
            self.nextToken()

            if (self.tokenC == '['):
                self.nextToken()
                result += self.compileExpression()
                self.nextToken()
            elif (self.tokenC == '.'):
                self.nextToken()
                self.auxClassName = id
                result += self.compileTerm()
            elif (self.tokenC == '('):
                self.nextToken()
                self.countArg = 0
                result += self.compileExpressionList()
                result += self.vm.writeCall(self.auxClassName+'.'+id, self.countArg)
                self.nextToken()
            else:
                result += self.vm.writePush(self.vm.kindOf(id), self.vm.indexOf(id))
        elif (self.tokenT == 'stringConst'):
            string = self.tokenC[1:-1]
            result += self.vm.writePush('constant', len(string)) # por conta das ""
            result += self.vm.writeCall('String.new', 1)

            for i in string:
                result += self.vm.writePush('constant', ord(i))
                result += self.vm.writeCall('String.appendChar', 2)

            self.nextToken()
        elif(self.tokenT == 'symbol'):
            if (self.tokenC == '('):
                self.nextToken()
                result += self.compileExpressionList()
                self.nextToken()
            elif (self.tokenC in self.unaryOp):
                unaryOP = self.tokenC
                self.nextToken()
                result += self.compileTerm()
                result += self.vm.writeArithmetic(unaryOP)
        elif(self.tokenT == 'keyword'):
            if (self.tokenC == 'this'):
                result += self.vm.writePush('pointer', 0)
                self.nextToken()
                self.nextToken()

        return result

    def compileExpressionList(self):
    # compila uma lista de expressão
        if (self.tokenC == ')'):
            return ''
        else:
            self.countArg += 1
            result = self.compileExpression()

            if (self.tokenC == ','):
                self.nextToken()
                result += self.compileExpressionList()

            return result

test = VMCompileEngine("""// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/11/ComplexArrays/Main.jack

/**
 * Performs several complex array processing tests.
 * For each test, the expected result is printed, along with the
 * actual result. In each test, the two results should be equal.
 */
class Main {

    function void main() {
        var Array a, b, c;
        
        let a = Array.new(10);
        let b = Array.new(5);
        let c = Array.new(1);
        
        let a[3] = 2;
        let a[4] = 8;
        let a[5] = 4;
        let b[a[3]] = a[3] + 3;  // b[2] = 5
        let a[b[a[3]]] = a[a[5]] * b[((7 - a[3]) - Main.double(2)) + 1];  // a[5] = 8 * 5 = 40
        let c[0] = null;
        let c = c[0];
        
        do Output.printString("Test 1: expected result: 5; actual result: ");
        do Output.printInt(b[2]);
        do Output.println();
        do Output.printString("Test 2: expected result: 40; actual result: ");
        do Output.printInt(a[5]);
        do Output.println();
        do Output.printString("Test 3: expected result: 0; actual result: ");
        do Output.printInt(c);
        do Output.println();
        
        let c = null;

        if (c = null) {
            do Main.fill(a, 10);
            let c = a[3];
            let c[1] = 33;
            let c = a[7];
            let c[1] = 77;
            let b = a[3];
            let b[1] = b[1] + c[1];  // b[1] = 33 + 77 = 110;
        }

        do Output.printString("Test 4: expected result: 77; actual result: ");
        do Output.printInt(c[1]);
        do Output.println();
        do Output.printString("Test 5: expected result: 110; actual result: ");
        do Output.printInt(b[1]);
        do Output.println();
        return;
    }
    
    function int double(int a) {
    	return a * 2;
    }
    
    function void fill(Array a, int size) {
        while (size > 0) {
            let size = size - 1;
            let a[size] = Array.new(3);
        }
        return;
    }
}
""")
print(test.compile())