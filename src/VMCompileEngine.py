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
        self.subroutineName = ''

        self.countArg = 0
        self.countWhile = 0
        self.countIf = 0


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
            self.subroutineName = self.tokenC
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
            # self.countMethod += 1
            # print(self.tokenC)
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
        elif(self.tokenT == 'identifier'):
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

        count = 0
        for i in self.vm.tableSymbolSR:
            if ('local' == i['kind']):
                count += 1
                
        result = 'function ' + self.className + '.' + self.subroutineName + ' ' + str(count) + '\n'
        # print(self.tokenC)
        result += self.compileStatements()
        # print(self.tokenC)
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
        array = False
        temp = 0

        self.nextToken() # tokenC = identificador
        id = self.tokenC
        # print(id)
        self.nextToken()

        if (self.tokenC == '['):
            array = True
            self.nextToken()
            result += self.compileExpression()
            self.esperado(']') # tokenC = ]
            result += self.vm.writePush(self.vm.kindOf(id), self.vm.indexOf(id))
            result += self.vm.writeArithmetic('+')
            self.nextToken()

        self.esperado('=') # tokenC = =
        self.nextToken()
        # print(self.tokenC)
        result += self.compileExpression()
        # print(result)
        # print(self.tokenC)
        self.esperado(';') # tokenC = ;
        self.nextToken()

        if (array == True):
            result += self.vm.writePop('temp', temp)
            result += self.vm.writePop('pointer', 1)
            result += self.vm.writePush('temp', temp)
            result += self.vm.writePop('that', 0)
            # result += self.vm.writePush('constant', 0)
            temp += 1
        else:
            result += self.vm.writePop(self.vm.kindOf(id), self.vm.indexOf(id))
        
        return result

    def compileIf(self):
    # compila um Statement If
        result = ''
        self.nextToken()
        
        label1 = 'IF_TRUE' + str(self.countIf)
        label2 = 'IF_FALSE' + str(self.countIf)
        label3 = 'IF_END'+ str(self.countIf)

        self.esperado('(')
        self.nextToken()
        result += self.compileExpression()
        self.esperado(')')
        self.nextToken()
        # print(self.tokenC)
        
        result += self.vm.writeIf(label1) # if-goto L1
        result += self.vm.writeGoto(label2) # goto L2
        result += self.vm.writeLabel(label1) # L1

        self.esperado('{')
        self.nextToken()
        self.countIf += 1
        result += self.compileStatements()
        self.countIf = self.countIf - 1
        self.esperado('}')
        self.nextToken()

        if (self.tokenC == 'else'):
            result += self.vm.writeGoto(label3) # goto END
            result += self.vm.writeLabel(label2) # L2

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

        label1 = 'WHILE_EXP' + str(self.countWhile)
        label2 = 'WHILE_END' + str(self.countWhile)

        result += self.vm.writeLabel(label1) # L WHILE EXP

        self.nextToken()
        self.esperado('(')
        self.nextToken()
        self.countWhile += 1
        result += self.compileExpression()
        self.countWhile = self.countWhile - 1
        self.esperado(')')

        result += self.vm.writeArithmetic('~')
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
        self.nextToken()
        result = self.compileExpression()
        # print(result)
        # print(self.tokenC)
        self.esperado(';')
        self.nextToken()
        result += self.vm.writePop('temp', 0)
        
        return result

    def compileReturn(self):
    # compila um Statement Return
        result = ''
        self.nextToken()

        if (self.tokenC != ';'):
            result += self.compileExpression()
            self.nextToken()
        else:
            self.nextToken()
            result += self.vm.writePush('constant', 0)

        result += self.vm.writeReturn()
        return result

    def compileExpression(self):
    # compila uma expressão
        result = self.compileTerm()
        # self.nextToken()

        while self.tokenC in self.op:
            op = self.tokenC
            self.nextToken()
            result += self.compileTerm()

            if (op == '*'):
                result += self.vm.writeCall('Math.multiply', 2)
            elif (op == '/'):
                result += self.vm.writeCall('Math.divide', 2)
            # elif (op == ','):
            #     result += self.compileExpressionList()
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

                result += self.vm.writePush(self.vm.kindOf(id), self.vm.indexOf(id))
                result += self.vm.writeArithmetic('+')
                result += self.vm.writePop('pointer', 1)
                result += self.vm.writePush('that', 0)

            elif (self.tokenC == '.'):
                self.nextToken()
                self.auxClassName = id
                result += self.compileTerm()
            elif (self.tokenC == '('):
                self.nextToken()
                self.countArg = 0
                result += self.compileExpressionList()
                self.esperado(')')
                self.nextToken()
                result += self.vm.writeCall(self.auxClassName+'.'+id, self.countArg)
            else:
                result += self.vm.writePush(self.vm.kindOf(id), self.vm.indexOf(id))
        elif (self.tokenT == 'stringConst'):
            string = self.tokenC[1:-1] # removendo as ""
            result += self.vm.writePush('constant', len(string))
            result += self.vm.writeCall('String.new', 1)

            for i in string:
                result += self.vm.writePush('constant', ord(i))
                result += self.vm.writeCall('String.appendChar', 2)

            self.nextToken()
        elif(self.tokenT == 'symbol'):
            if (self.tokenC == '('):
                self.nextToken()
                # if (self.tokenC == '('):
                #     self.nextToken()
                #     result += self.compileExpression()
                #     self.nextToken()
                # else:
                #     self.countArg = 0
                #     result += self.compileExpressionList()
                #     self.nextToken()
                result += self.compileExpression()
                self.esperado(')')
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
            elif (self.tokenC == 'null'):
                result += self.vm.writePush('constant', 0)
                self.nextToken()
            elif (self.tokenC == 'true'):
                result += self.vm.writePush('constant', 0)
                result += self.vm.writeArithmetic('~')
                self.nextToken()
            elif (self.tokenC == 'false'):
                result += self.vm.writePush('constant', 0)
                self.nextToken()
            else:
                self.nextToken()

        return result

    def compileExpressionList(self):
    # compila uma lista de expressão
        if (self.tokenC == ')'):
            # self.nextToken()
            return ''
        else:
            self.countArg += 1
            result = self.compileExpression()
            # self.nextToken()
            # print(self.tokenC)

            if (self.tokenC == ','):
                self.nextToken()
                if (self.tokenC == '-'):
                    self.nextToken()
                    result += self.compileExpressionList()
                    result += self.vm.writeArithmetic('neg')
                else:
                    result += self.compileExpressionList()
            elif (self.tokenC == '-'):
                self.nextToken()
                result += self.compileExpressionList()
                result += self.vm.writeArithmetic('neg')

            return result

test = VMCompileEngine("""
// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/11/Pong/PongGame.jack

/**
 * Represents a Pong game.
 */
class PongGame {

    static PongGame instance; // the singelton, a Pong game instance     
    field Bat bat;            // the bat
    field Ball ball;          // the ball
    field int wall;           // the current wall that the ball is bouncing off of.
    field boolean exit;       // true when the game is over
    field int score;          // the current score.
    field int lastWall;       // the last wall that the ball bounced off of.

    // The current width of the bat
    field int batWidth;

    /** Constructs a new Pong game. */
    constructor PongGame new() {
	    do Screen.clearScreen();
        let batWidth = 50;  // initial bat size
        let bat = Bat.new(230, 229, batWidth, 7);
        let ball = Ball.new(253, 222, 0, 511, 0, 229);
        do ball.setDestination(400,0);
        do Screen.drawRectangle(0, 238, 511, 240);
	    do Output.moveCursor(22,0);
	    do Output.printString("Score: 0");
	
	    let exit = false;
	    let score = 0;
	    let wall = 0;
	    let lastWall = 0;

        return this;
    }

    /** Deallocates the object's memory. */
    method void dispose() {
        do bat.dispose();
	    do ball.dispose();
        do Memory.deAlloc(this);
        return;
    }

    /** Creates an instance of Pong game, and stores it. */
    function void newInstance() {
        let instance = PongGame.new();
        return;
    }
    
    /** Returns the single instance of this Pong game. */
    function PongGame getInstance() {
        return instance;
    }

    /** Starts the game, and andles inputs from the user that control
     *  the bat's movement direction. */
    method void run() {
        var char key;

        while (~exit) {
            // waits for a key to be pressed.
            while ((key = 0) & (~exit)) {
                let key = Keyboard.keyPressed();
                do bat.move();
                do moveBall();
                do Sys.wait(50);
            }

            if (key = 130) { do bat.setDirection(1); }
	        else {
	            if (key = 132) { do bat.setDirection(2); }
		        else {
                    if (key = 140) { let exit = true; }
		        }
            }

            // Waits for the key to be released.
            while ((~(key = 0)) & (~exit)) {
                let key = Keyboard.keyPressed();
                do bat.move();
                do moveBall();
                do Sys.wait(50);
            }
        }

	    if (exit) {
            do Output.moveCursor(10,27);
	        do Output.printString("Game Over");
	    }
            
        return;
    }

    /**
     * Handles ball movement, including bouncing.
     * If the ball bounces off a wall, finds its new direction.
     * If the ball bounces off the bat, increases the score by one
     * and shrinks the bat's size, to make the game more challenging. 
     */
    method void moveBall() {
        var int bouncingDirection, batLeft, batRight, ballLeft, ballRight;

        let wall = ball.move();

        if ((wall > 0) & (~(wall = lastWall))) {
            let lastWall = wall;
            let bouncingDirection = 0;
            let batLeft = bat.getLeft();
            let batRight = bat.getRight();
            let ballLeft = ball.getLeft();
            let ballRight = ball.getRight();
  
            if (wall = 4) {
                let exit = (batLeft > ballRight) | (batRight < ballLeft);
                if (~exit) {
                    if (ballRight < (batLeft + 10)) { let bouncingDirection = -1; }
                    else {
                        if (ballLeft > (batRight - 10)) { let bouncingDirection = 1; }
                    }

                    let batWidth = batWidth - 2;
                    do bat.setWidth(batWidth);      
                    let score = score + 1;
                    do Output.moveCursor(22,7);
                    do Output.printInt(score);
                }
            }
            do ball.bounce(bouncingDirection);
        }
        return;
    }
}
""")

print(test.compile())
# test.compile()