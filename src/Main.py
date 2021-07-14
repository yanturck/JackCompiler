import JackTokenizer as lexer
import CompilationEngine as eng

class JackCompiler:
    def __init__(self):
        self.fname = open('Square.jack', 'r')
        self.lname = open('SquareT.xml', 'w')
        self.sname = open('Square.xml', 'w')

        self.prog = self.fname.read()

        self.lexer = lexer.JackTokenizer(self.prog)
        self.sinta = eng.CompilationEngine(self.prog)

        self.lname.write('<tokens>\n')
        while (self.lexer.hasMoreTokens() == True):
            self.lexer.advance()
            token = self.lexer.getToken()
            self.lname.write(self.lexer.tagToken(token))

        self.lname.write('</tokens>')
        self.lname.close()

        self.sname.write(self.sinta.compile())
        self.sname.close()

JackCompiler()