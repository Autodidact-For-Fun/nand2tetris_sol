def read_vmfile(path):
    """
    use open read file and return read content as a list and drop comments
    """
    with open(path, 'r') as f:
        content = f.readlines()
        content = [line.strip() for line in content
                   if line.strip() and line[0] != '/']
    return content


def write_asmfile(asm_codes, path):
    """
    write list item with endline to file
    """
    with open(path, 'w') as f:
        for code in asm_codes:
            f.write(code + '\n')
    return


def push_to_asm(code, filename):
    """
    implement push_to_asm function"""
    segments = ['SP', 'local', 'argument', 'this', 'that']
    segment = code.split("/")[0].split(' ')[1]
    i = code.split(' ')[2]
    # branch_to_asm(code)
    if segment == 'constant':
        # push constant: *SP = constant, SP++
        return '@{}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1'.format(code.split(' ')[2])
    elif segment in segments:
        # push segment: addr=segment_base + index, *SP=*addr, SP++
        return '@{}\nD=M\n@{}\nD=D+A\nA=D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1' \
               .format('R{}'.format(segments.index(segment)), i)
    elif segment == 'temp':
        # push temp: addr=5 + index, *SP=*addr, SP++
        return '@5\nD=A\n@{}\nD=D+A\nA=D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1' \
               .format(i)
    elif segment == 'pointer':
        # push pointer: *SP=*this/that, SP++
        if code.split(' ')[2] == '0':
            return '@R3\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1'
        else:
            return '@R4\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1'
    elif segment == 'static':
        # push static: *SP=*addr, SP++
        print('push {} {}'.format(filename, i))
        return '@{}.{}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1'.format(filename, i)

def branch_to_asm(code):
    # branch_to_asm(code)
    name = code.split("/")[0].split(' ')[1]
    if "label" in code:
        return '({})'.format(name)
    elif "if-goto" in code:
        return '@SP\nM=M-1\nA=M\nD=M\n@{}\nD;JGT\n@{}\nD;JLT'.format(name, name)
    elif "goto" in code:
        return '@{}\n0;JMP'.format(name)
    
def function_to_asm(code):
    name = code.split("/")[0].split(' ')[1]
    nVars = int(code.split("/")[0].split(' ')[2])
    function_label = '({})\n'.format(name)
    local_vars = ''
    for i in range(nVars):
        local_vars += (push_to_asm("push constant 0", "xxx") + '\n')
    
    return function_label + local_vars
    
def return_to_asm(code, i):
    return '@5\nD=A\n@LCL\nD=M-D\nA=D\nD=M\n@retAddr{}\nM=D\n \
            @SP\nM=M-1\nA=M\nD=M\n@ARG\nA=M\nM=D\n@ARG\nD=M\n@SP\nM=D+1\n \
            @1\nD=A\n@LCL\nD=M-D\nA=D\nD=M\n@THAT\nM=D\n \
            @2\nD=A\n@LCL\nD=M-D\nA=D\nD=M\n@THIS\nM=D\n \
            @3\nD=A\n@LCL\nD=M-D\nA=D\nD=M\n@ARG\nM=D\n \
            @4\nD=A\n@LCL\nD=M-D\nA=D\nD=M\n@LCL\nM=D\n \
            @retAddr{}\nA=M\n0;JMP'.format(i, i)
            
def call_to_asm(code, i):
    name = code.split("/")[0].split(' ')[1]
    nVars = int(code.split("/")[0].split(' ')[2])
    gotoname = 'goto ' + name
    
    return '@callreturn{}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n \
            @LCL\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n \
            @ARG\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n \
            @THIS\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n \
            @THAT\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n \
            @5\nD=A\n@{}\nD=A+D\n@SP\nD=M-D\n@ARG\nM=D\n \
            @SP\nD=M\n@LCL\nM=D\n \
            '.format(i, nVars) + branch_to_asm(gotoname) + '\n(callreturn{})'.format(i)
            
def pop_to_asm(code, filename):
    """
    implement pop_to_asm function"""
    # branch_to_asm(code)
    segments = ['SP', 'local', 'argument', 'this', 'that']
    segment = code.split("/")[0].split(' ')[1]
    i = code.split(' ')[2]
    if segment in segments:
        # pop segment: addr=segment_base + index, SP--, *addr=*SP
        return '@{}\nD=M\n@{}\nD=D+A\n@addr\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@addr \
                \nA=M\nM=D'.format('R{}'.format(segments.index(segment)), i)
    elif segment == 'temp':
        # pop temp: addr=5 + index, SP--, *addr=*SP
        return '@5\nD=A\n@{}\nD=D+A\n@addr\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@addr \
                \nA=M\nM=D'.format(i)
    elif segment == 'pointer':
        # pop pointer: SP--, *this/that=*SP
        if code.split(' ')[2] == '0':
            return '@SP\nM=M-1\nA=M\nD=M\n@R3\nM=D'
        else:
            return '@SP\nM=M-1\nA=M\nD=M\n@R4\nM=D'
    elif segment == 'static':
        # pop static: SP--, *addr=*SP
        print('pop {} {}'.format(filename, i))
        return '@SP\nM=M-1\nA=M\nD=M\n@{}.{}\nM=D'.format(filename, i)


def add_to_asm(code):
    """
    implement add_to_asm function"""
    return '@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nM=M+D\n@SP\nM=M+1'


def sub_to_asm(code):
    """
    implement sub_to_asm function"""
    return '@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nM=M-D\n@SP\nM=M+1'


def eq_to_asm(code, i):
    """
    implement sub_to_asm function"""
    return '@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nD=M-D\n@EQ.{}\nD;JEQ\n \
            @SP\nA=M\nM=0\n@SP\nM=M+1\n@END.{}\n0;JMP\n(EQ.{})\n@SP\nA=M\n \
                M=-1\n@SP\nM=M+1\n(END.{})'.format(i, i, i, i)


def lt_to_asm(code, i):
    """
    implement sub_to_asm function"""
    return '@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nD=M-D\n@LT.{}\nD;JLT\n \
            @SP\nA=M\nM=0\n@SP\nM=M+1\n@END.{}\n0;JMP\n(LT.{})\n@SP\nA=M\n \
                M=-1\n@SP\nM=M+1\n(END.{})'.format(i, i, i, i)


def gt_to_asm(code, i):
    """
    implement sub_to_asm function"""
    return '@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nD=M-D\n@GT.{}\nD;JGT\n \
            @SP\nA=M\nM=0\n@SP\nM=M+1\n@END.{}\n0;JMP\n(GT.{})\n@SP\nA=M\n \
                M=-1\n@SP\nM=M+1\n(END.{})'.format(i, i, i, i)


def and_to_asm(code):
    """
    implement sub_to_asm function"""
    return '@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nM=M&D\n@SP\nM=M+1'


def not_to_asm(code):
    """
    implement sub_to_asm function"""
    return '@SP\nM=M-1\nA=M\nM=!M\n@SP\nM=M+1'


def or_to_asm(code):
    """
    implement sub_to_asm function"""
    return '@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nM=M|D\n@SP\nM=M+1'


def neg_to_asm(code):
    """
    implement sub_to_asm function"""
    return '@SP\nM=M-1\nA=M\nM=-M\n@SP\nM=M+1'


def vm_to_assmble(code_list, filename):
    """
    translate pop code to assembly code"""
    asm_codes = []
    asm_codes.append('@256\nD=A\n@SP\nM=D\n')
    fn = filename
    for i, code in enumerate(code_list):
        if code.startswith('push'):
            asm_codes.append(push_to_asm(code, fn))
        elif code.startswith('pop'):
            asm_codes.append(pop_to_asm(code, fn))
        elif code.startswith('add'):
            asm_codes.append(add_to_asm(code))
        elif code.startswith('sub'):
            asm_codes.append(sub_to_asm(code))
        elif code.startswith('eq'):
            asm_codes.append(eq_to_asm(code, i))
        elif code.startswith('lt'):
            asm_codes.append(lt_to_asm(code, i))
        elif code.startswith('gt'):
            asm_codes.append(gt_to_asm(code, i))
        elif code.startswith('and'):
            asm_codes.append(and_to_asm(code))
        elif code.startswith('or'):
            asm_codes.append(or_to_asm(code))
        elif code.startswith('not'):
            asm_codes.append(not_to_asm(code))
        elif code.startswith('neg'):
            asm_codes.append(neg_to_asm(code))
        elif code.startswith('label') or code.startswith('goto') or code.startswith('if-goto'):
            asm_codes.append(branch_to_asm(code))
        elif code.startswith('function'):
            asm_codes.append(function_to_asm(code))
        elif code.startswith('return'):
            asm_codes.append(return_to_asm(code, i))
        elif code.startswith('call'):
            asm_codes.append(call_to_asm(code, i))
    return asm_codes
