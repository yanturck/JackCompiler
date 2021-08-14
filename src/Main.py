import VMCompileEngine as vm
import os

class JackCompiler:
    def __init__(self):
        self.caminhos = [os.path.join('/home/yan/Documentos/Compiladores/nand2tetris/projects/11/Average', nome) for nome in os.listdir('/home/yan/Documentos/Compiladores/nand2tetris/projects/11/Average')]
        self.arqJack = [arq for arq in self.caminhos if arq.lower().endswith(".jack")]

        while self.arqJack != []:
            fpath = self.arqJack.pop()
            fname = open(fpath, 'r')
            vname = open(fpath[:-4] + 'vm', 'w')

            vmcode = vm.VMCompileEngine(fname.read())
            vname.write(vmcode.compile())

JackCompiler()