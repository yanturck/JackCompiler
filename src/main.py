import lexer

class JackCompiler:
    def __init__(self):
        self.fname = open('Square.jack', 'r')
        self.rname = open('Square.xml', 'w')

        self.lexer = lexer.JackTokenizer(self.fname.read())

        self.rname.write('<tokens>\n')
        while (self.lexer.hasMoreTokens() == True):
            self.lexer.advance()
            token = self.lexer.getToken()
            tokenType = self.lexer.tokenType(token)
            self.rname.write('<'+tokenType+'> ' + self.lexer.getToken() + ' </'+tokenType+'>\n')

        self.rname.write('</tokens>')
        self.rname.close()

JackCompiler()