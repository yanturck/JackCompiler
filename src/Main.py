import JackTokenizer as lexer
import CompilationEngine as eng
import os

class JackCompiler:
    def __init__(self):
        self.caminhos = [os.path.join('/home/yan/Documentos/Compiladores/nand2tetris/projects/10/ExpressionLessSquare/Testes', nome) for nome in os.listdir('/home/yan/Documentos/Compiladores/nand2tetris/projects/10/ExpressionLessSquare')]
        self.arqJack = [arq for arq in self.caminhos if arq.lower().endswith(".jack")]

        while self.arqJack != []:
            fpath = self.arqJack.pop()
            fname = open(fpath, 'r')
            sname = open(fpath[:-4] + 'xml', 'w')

            sinta = eng.CompilationEngine(fname.read())
            sname.write(sinta.compile())

JackCompiler()