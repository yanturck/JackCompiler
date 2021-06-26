import lexer

class JackCompiler:
    def __init__(self):
        self.fname = '''if (x < 0) {
        // prints the sign
        let sign = "Massa";
        // this new comentario
        }'''

        self.lexer = lexer.JackTokenizer(self.fname)

        print('<tokens>')
        while (self.lexer.hasMoreTokens() == True):
            self.lexer.advance()
            token = self.lexer.getToken()
            tokenType = self.lexer.tokenType(token)
            print('<'+tokenType+'> ' + self.lexer.getToken() + ' </'+tokenType+'>')

        print('</tokens>')

JackCompiler()