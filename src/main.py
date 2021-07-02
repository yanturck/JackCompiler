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
            
            if (token == '&'): # substituindo simbolo
                self.rname.write('<'+tokenType+'> ' + '&amp;' + ' </'+tokenType+'>\n')
            elif (token == '>'): # substituindo simbolo
                self.rname.write('<'+tokenType+'> ' + '&gt;' + ' </'+tokenType+'>\n')
            elif (token == '<'): # substituindo simbolo
                self.rname.write('<'+tokenType+'> ' + '&lt;' + ' </'+tokenType+'>\n')
            elif (tokenType == 'stringConst'):
                self.rname.write('<'+tokenType+'> ' + token[1:len(token)-1] + ' </'+tokenType+'>\n')
            else:
                self.rname.write('<'+tokenType+'> ' + token + ' </'+tokenType+'>\n')

        self.rname.write('</tokens>')
        self.rname.close()

JackCompiler()