import sys


symbolTable = {
    'SP': '0',
    'LCL': '1',
    'ARG': '2',
    'THIS': '3',
    'THAT': '4',
    'SCREEN': '16384',
    'KBD': '24576',
}

for i in range(0, 16):
    label = 'R' + str(i)
    symbolTable[label] = i


class Assembler:
    def assemble(self, file_name):
        self.file_name = file_name
        asm_lists = Parser.Advance(file_name) 
        
        print(file_name[:-4])
        outfile = open(file_name[:-4]+'.hack', 'w')

        num = 0
        val_sym = 16
        for i in asm_lists:
            if Parser.commandType(i) == 'C_COMMAND':
                num += 1
            elif Parser.commandType(i) == 'A_COMMAND':
                num += 1
            else:
                Parser.parse_L(self, i, num)

        for i in asm_lists:
            if Parser.commandType(i) == 'C_COMMAND':
                print(Parser.parse_C(i))
                outfile.write(Parser.parse_C(i) + '\n')
            elif Parser.commandType(i) == 'A_COMMAND':
                if i[1:] not in symbolTable.keys():
                    symbolTable[i[1:]] = val_sym
                    val_sym += 1
                print(Parser.parse_A(self, i))
                outfile.write(Parser.parse_A(self, i)+'\n') 
        outfile.close()     

class Parser:
    def Advance(file_name):
        raw_asm_file = open(file_name)
        asm_lines = raw_asm_file.read()
        raw_asm_file.close()
        lines = asm_lines.splitlines()
        asm_list = []
        for l in lines:
            l_nospace = l.replace(' ', '')
            #if l[:2] != '//' and l != '' and l[:1] != '(':
            if l[:2] != '//' and l != '': 
                comment_num = l_nospace.find('//') 
                if comment_num == -1:
                    asm_list.append(l_nospace)
                else:
                    asm_list.append(l_nospace[:comment_num])
        return asm_list
        
    def commandType(mnemonic):
        if mnemonic[:1] == '@':
            return 'A_COMMAND'
        elif mnemonic[:1] == '(':
            return 'L_COMMAND'
        else:
            return 'C_COMMAND'

    def parse_A(self, mnemonic):
        self.mnemonic = mnemonic
        symbol = mnemonic[1:]
        return SymbolTable.symbol(self, symbol)  

    def parse_C(mnemonic):
        dest_bit = ''
        comp_bit = ''
        jump_bit = ''
        if '=' in mnemonic:
            dest_bit, comp_bit = mnemonic.split('=')
            if ';' in comp_bit:
                comp_bit, jump_bit = comp_bit.split(';')
        elif ';' in mnemonic:
            comp_bit, jump_bit = mnemonic.split(';')
        d_bit = Code.dest(dest_bit)
        c_bit = Code.comp(comp_bit)
        j_bit = Code.jump(jump_bit)
        return '111' + c_bit + d_bit + j_bit

    def parse_L(self, mnemonic, num):
        self.mnemonic = mnemonic
        symbol = self.mnemonic[1:-1]
        SymbolTable.addEntry(self,symbol, num)

class Code:
    def dest(mnemonic):
        d_bit = ['0', '0', '0']
        if 'M' in mnemonic:
            d_bit[2] = '1'
        elif 'D' in mnemonic:
            d_bit[1] = '1'
        elif 'A' in mnemonic:
            d_bit[0] = '1'
        return ''.join(d_bit)


    def comp(mnemonic):
        comp_dict = {
            '0': '101010',
            '1': '111111',
            '-1': '111010',
            'D': '001100',
            'A': '110000',
            '!D': '001101',
            '!A': '110001',
            '-D': '001111',
            '-A': '110011',
            'D+1': '011111',
            'A+1': '110111',
            'D-1': '001110',
            'A-1': '110010',
            'D+A': '000010',
            'D-A': '010011',
            'A-D': '000111',
            'D&A': '000000',
            'D|A': '010101',
        }

        a_bit = '0'
        if 'M' in mnemonic:
            a_bit = '1'
            mnemonic = mnemonic.replace('M', 'A')
        c_bit = comp_dict.get(mnemonic, '000000')
        return a_bit + c_bit 


    def jump(mnemonic):
        jump_dict = {
            'JGT': '001',
            'JEQ': '010',
            'JGE': '011',
            'JLT': '100',
            'JNE': '101',
            'JLE': '110',
            'JMP': '111',
        }
        return jump_dict.get(mnemonic, '000')


class SymbolTable:
    def symbol(self,symbol):
        self.symbol = symbol
        if self.symbol.isdecimal():
            return format(int(self.symbol), '016b')
        else:
            return format(symbolTable.get(symbol,0),'016b')


    def addEntry(self, symbol, num):
        self.symbol = symbol        
        if self.symbol not in symbolTable.keys():
            symbolTable[self.symbol] = num


if __name__ == '__main__':
    file_name = sys.argv[1]
    assembler = Assembler()
    assembler.assemble(file_name)
