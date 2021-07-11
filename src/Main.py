import JackTokenizer as lexer

class JackCompiler:
    def __init__(self):
        self.fname = open('Square.jack', 'r')
        self.rname = open('Square.xml', 'w')

        self.lexer = lexer.JackTokenizer(self.fname.read())

        self.rname.write('<tokens>\n')
        while (self.lexer.hasMoreTokens() == True):
            self.lexer.advance()
            token = self.lexer.getToken()
            self.rname.write(self.lexer.tagToken(token))

        self.rname.write('</tokens>')
        self.rname.close()

JackCompiler()