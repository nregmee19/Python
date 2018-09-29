""" CS 3339 Project 1 
by Matthew Presley and Niraj Regmee
"""
import sys

class MipsMaster:

    memory = []
    PC = 96
    instruction = []
    opcode = []
    validInstr = []
    address = []
    arg1 = []
    arg2 = []
    arg3 = []
    numInstructions = 0
    cycle = 1
    R = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

    """
    def __init__ (self, instrs, opcodes, mem, valids, addrs, args1, args2, args3, numInstrs):
        self.instruction = instrs
        self.opcode = opcodes
        self.memory = mem
        self.validInstr = valids
        self.address = addrs
        self.numInstructions = numInstrs
        self.arg1 = args1
        self.arg2 = args2
        self.arg3 = args3
    """

    def twoscomplement(self, value):
        i = 0
        newvalue = ""
        while(i < len(value)):
            b=value[i]
            if (b=='0'):
                newvalue = newvalue+'1'
            else: 
                newvalue = newvalue+'0'
            i = i+1
        i= i-1
        b= newvalue[i]
        while (b == '1'):
            i = i-1
            b= newvalue[i]
        addlast = newvalue[i:32]
        lastbits= ""
        j = 0
        while(j < len(addlast)):
            b=addlast[j]
            if (b=='0'):
                lastbits = lastbits+'1'
            else:
                lastbits = lastbits+'0'
            j = j+1
            newvalue = newvalue[:i]+lastbits
        return newvalue
    	
    def bitconverter(value):
        i = 0
        newvalue = ""
        while(i < len(value)):
            b=value[i]
            if (b=='0'):
                newvalue = newvalue+'1'
            else:
                newvalue = newvalue+'0'
            i = i+1
        return newvalue
    	
    def subone(value):
        newvalue = ""
        i = len(value)-1
        b= value[i]
        while (b == '0'):
            i = i-1
            b= value[i]
        addlast = value[i:]
        lastbits= bitconverter(addlast)
        newvalue = value[:i]+lastbits
        return newvalue
    	
    def twosconverter(self, value):
        temp = subone(value)
        newvalue = bitconverter(temp)
        return newvalue

    def bintodec(self, value):
        num = 0
        i = len(value)-1
        pos  = 0
        while (i > 0):
            b = value[i]
            if b == '1':
                num = num+ (2**pos)
            i = i-1
            pos = pos+1
        return num
        
    def shifttwo(self, value):
        newValue = value + '00'
        return newValue
    
def main():
    #start of dissassembler
    for i in range(len (sys.argv)):
        if (sys.argv[i] == '-i' and i < (len(sys.argv)-1)): #confirms 2 args
            inputFileName = sys.argv[i+1]
        elif (sys.argv[i] == '-o' and i < (len(sys.argv)-1)):
            outputFileName = sys.argv[i+1]
    outFileD = open(outputFileName + "_dis.txt", 'w')
    outFileS = open(outputFileName + "_sim.txt", 'w')

    proj = MipsMaster()
    instructions = [line.rstrip() for line in open(inputFileName,'rb')]
    br = False
    i = 0
    while (i < len(instructions)):
        tempstr = instructions[i]
        if (br == False):
            if (tempstr == ''):
                proj.PC = proj.PC
            elif (tempstr[0] == '0'):
                outFileD.write('%s %s %s %s %s %s %s\t%r%s' \
                % (tempstr[0],tempstr[1:6],tempstr[6:11],tempstr[11:16], \
                tempstr[16:21],tempstr[21:26],tempstr[26:],proj.PC,\
                '\tInvalid Instruction\n'))
                proj.PC = proj.PC + 4
            else:
                if (tempstr[1:6] == '01000'): #ADDI
                    if tempstr[16] == '0':
                        outFileD.write('%s %s %s %s %s %s %s\t%r\t%s\t%s%r, %s%r, #%r\n' \
                        % (tempstr[0],tempstr[1:6],tempstr[6:11],tempstr[11:16], \
                        tempstr[16:21],tempstr[21:26],tempstr[26:],proj.PC, 'ADDI','R', \
                        proj.bintodec(tempstr[11:16]), 'R', proj.bintodec(tempstr[6:11]),\
                        proj.bintodec(tempstr[16:])))
                    else:
                        twos = proj.twoscomplement(tempstr[16:])
                        outFileD.write('%s %s %s %s %s %s %s\t%r\t%s\t%s%r, %s%r, #-%r\n'\
                        % (tempstr[0],tempstr[1:6],tempstr[6:11],tempstr[11:16], \
                        tempstr[16:21],tempstr[21:26],tempstr[26:],proj.PC, 'ADDI','R', \
                        proj.bintodec(tempstr[11:16]), 'R', proj.bintodec(tempstr[6:11]),\
                        proj.bintodec(twos)))
                    proj.PC = proj.PC + 4
                elif (tempstr[1:6] == '01011'): #SW
                    if tempstr[16] == '0':
                        outFileD.write('%s %s %s %s %s %s %s\t%r\t%s\t%s%r, %r(%s%r)\n' \
                        % (tempstr[0],tempstr[1:6],tempstr[6:11],tempstr[11:16], \
                        tempstr[16:21],tempstr[21:26],tempstr[26:],proj.PC, 'SW','R', \
                        proj.bintodec(tempstr[11:16]), proj.bintodec(tempstr[16:]), 'R',\
                        proj.bintodec(tempstr[6:11])))
                    else:
                        twos = proj.twoscomplement(tempstr[16:])
                        outFileD.write('%s %s %s %s %s %s %s\t%r\t%s\t%s%r, %s%r, #-%r\n'\
                        % (tempstr[0],tempstr[1:6],tempstr[6:11],tempstr[11:16], \
                        tempstr[16:21],tempstr[21:26],tempstr[26:],proj.PC, 'SW','R', \
                        proj.bintodec(tempstr[11:16]), proj.bintodec(twos), 'R', \
                        proj.bintodec(tempstr[6:11])))
                    proj.PC = proj.PC + 4
                elif (tempstr[1:6] == '00011'): #LW
                    if tempstr[16] == '0':
                        outFileD.write('%s %s %s %s %s %s %s\t%r\t%s\t%s%r, %r(%s%r)\n' \
                        % (tempstr[0],tempstr[1:6],tempstr[6:11],tempstr[11:16], \
                        tempstr[16:21],tempstr[21:26],tempstr[26:],proj.PC, 'LW','R', \
                        proj.bintodec(tempstr[11:16]), proj.bintodec(tempstr[16:]), 'R',\
                        proj.bintodec(tempstr[6:11])))
                    else:
                        twos = proj.twoscomplement(tempstr[16:])
                        outFileD.write('%s %s %s %s %s %s %s\t%r\t%s\t%s%r, %s%r, #-%r\n'\
                        % (tempstr[0],tempstr[1:6],tempstr[6:11],tempstr[11:16], \
                        tempstr[16:21],tempstr[21:26],tempstr[26:],proj.PC, 'LW','R', \
                        proj.bintodec(tempstr[11:16]), proj.bintodec(twos), 'R', \
                        proj.bintodec(tempstr[6:11])))
                    proj.PC = proj.PC + 4
                elif (tempstr[1:6] == '00001'): #BLTZ
                    if tempstr[16] == '0':
                        shifted = proj.shifttwo(tempstr[16:])
                        outFileD.write('%s %s %s %s %s %s %s\t%r\t%s\t%s%r, #%r\n' \
                        % (tempstr[0],tempstr[1:6],tempstr[6:11],tempstr[11:16], \
                        tempstr[16:21],tempstr[21:26],tempstr[26:],proj.PC, 'BLTZ','R', \
                        proj.bintodec(tempstr[6:11]), proj.bintodec(shifted)))
                    else:
                        twos = proj.twoscomplement(tempstr[16:])
                        shifted = proj.shifttwo(twos)
                        outFileD.write('%s %s %s %s %s %s %s\t%r\t%s\t%s%r, #-%r\n' \
                        % (tempstr[0],tempstr[1:6],tempstr[6:11],tempstr[11:16], \
                        tempstr[16:21],tempstr[21:26],tempstr[26:],proj.PC, 'BLTZ','R', \
                        proj.bintodec(tempstr[6:11]), proj.bintodec(shifted)))
                    proj.PC = proj.PC + 4
                elif ((tempstr[1:6] == '00000') and (tempstr[26:] == '000000')): #SLL #NOP
                    if (tempstr[6:26] == '00000000000000000000'):
                        outFileD.write('%s %s %s %s %s %s %s\t%r\t%s\t%s%r, %s%r, #%r\n' \
                            % (tempstr[0],tempstr[1:6],tempstr[6:11],tempstr[11:16], \
                            tempstr[16:21],tempstr[21:26],tempstr[26:],proj.PC, 'NOP', \
                            'R', proj.bintodec(tempstr[16:21]), 'R', \
                            proj.bintodec(tempstr[11:16]), proj.bintodec(tempstr[21:26])))
                        proj.PC = proj.PC + 4
                    else:
                        outFileD.write('%s %s %s %s %s %s %s\t%r\t%s\t%s%r, %s%r, #%r\n' \
                            % (tempstr[0],tempstr[1:6],tempstr[6:11],tempstr[11:16], \
                            tempstr[16:21],tempstr[21:26],tempstr[26:],proj.PC, 'SLL', \
                            'R', proj.bintodec(tempstr[16:21]), 'R', \
                            proj.bintodec(tempstr[11:16]), proj.bintodec(tempstr[21:26])))
                        proj.PC = proj.PC + 4
                elif ((tempstr[1:6] == '00000') and (tempstr[26:] == '000010')): #SRL
                    outFileD.write('%s %s %s %s %s %s %s\t%r\t%s\t%s%r, %s%r, #%r\n' \
                        % (tempstr[0],tempstr[1:6],tempstr[6:11],tempstr[11:16], \
                        tempstr[16:21],tempstr[21:26],tempstr[26:],proj.PC, 'SRL','R', \
                        proj.bintodec(tempstr[16:21]), 'R', \
                        proj.bintodec(tempstr[11:16]), proj.bintodec(tempstr[21:26])))
                    proj.PC = proj.PC + 4
                elif ((tempstr[1:6] == '11100') and (tempstr[26:] == '000010')): #MUL
                    outFileD.write('%s %s %s %s %s %s %s\t%r\t%s\t%s%r, %s%r, %s%r\n' \
                        % (tempstr[0],tempstr[1:6],tempstr[6:11],tempstr[11:16], \
                        tempstr[16:21],tempstr[21:26],tempstr[26:],proj.PC, 'MUL','R', \
                        proj.bintodec(tempstr[16:21]), 'R', proj.bintodec(tempstr[6:11]),\
                        'R', proj.bintodec(tempstr[11:16])))
                    proj.PC = proj.PC + 4
                elif ((tempstr[1:6] == '00000') and (tempstr[26:] == '100100')): #AND
                    outFileD.write('%s %s %s %s %s %s %s\t%r\t%s\t%s%r, %s%r, %s%r\n' \
                        % (tempstr[0],tempstr[1:6],tempstr[6:11],tempstr[11:16], \
                        tempstr[16:21],tempstr[21:26],tempstr[26:],proj.PC, 'AND','R', \
                        proj.bintodec(tempstr[16:21]), 'R', proj.bintodec(tempstr[6:11]),\
                        'R', proj.bintodec(tempstr[11:16])))
                    proj.PC = proj.PC + 4
                elif ((tempstr[1:6] == '00000') and (tempstr[26:] == '100101')): #OR
                    outFileD.write('%s %s %s %s %s %s %s\t%r\t%s\t%s%r, %s%r, %s%r\n' \
                        % (tempstr[0],tempstr[1:6],tempstr[6:11],tempstr[11:16], \
                        tempstr[16:21],tempstr[21:26],tempstr[26:],proj.PC, 'OR','R', \
                        proj.bintodec(tempstr[16:21]), 'R', proj.bintodec(tempstr[6:11]),\
                        'R', proj.bintodec(tempstr[11:16])))
                    proj.PC = proj.PC + 4
                elif ((tempstr[1:6] == '00000') and (tempstr[26:] == '001010')): #MOVZ
                    outFileD.write('%s %s %s %s %s %s %s\t%r\t%s\t%s%r, %s%r, %s%r\n' \
                        % (tempstr[0],tempstr[1:6],tempstr[6:11],tempstr[11:16], \
                        tempstr[16:21],tempstr[21:26],tempstr[26:],proj.PC, 'MOVZ','R', \
                        proj.bintodec(tempstr[16:21]), 'R', proj.bintodec(tempstr[6:11]),\
                        'R', proj.bintodec(tempstr[11:16])))
                    proj.PC = proj.PC + 4
                elif ((tempstr[1:6] == '00000') and (tempstr[26:] == '100010')): #SUB
                    outFileD.write('%s %s %s %s %s %s %s\t%r\t%s\t%s%r, %s%r, %s%r\n' \
                        % (tempstr[0],tempstr[1:6],tempstr[6:11],tempstr[11:16], \
                        tempstr[16:21],tempstr[21:26],tempstr[26:],proj.PC, 'SUB','R', \
                        proj.bintodec(tempstr[16:21]), 'R', proj.bintodec(tempstr[6:11]),\
                        'R', proj.bintodec(tempstr[11:16])))
                    proj.PC = proj.PC + 4
                elif ((tempstr[1:6] == '00000') and (tempstr[26:] == '100000')): #ADD
                    outFileD.write('%s %s %s %s %s %s %s\t%r\t%s\t%s%r, %s%r, %s%r\n' \
                        % (tempstr[0],tempstr[1:6],tempstr[6:11],tempstr[11:16], \
                        tempstr[16:21],tempstr[21:26],tempstr[26:],proj.PC, 'ADD','R', \
                        proj.bintodec(tempstr[16:21]), 'R', proj.bintodec(tempstr[6:11]),\
                        'R', proj.bintodec(tempstr[11:16])))
                    proj.PC = proj.PC + 4
                elif (tempstr[1:6] == '00010'): #J
                    shifted = proj.shifttwo(tempstr[6:])
                    outFileD.write('%s %s %s %s %s %s %s\t%r\t%s\t#%r\n' \
                        % (tempstr[0],tempstr[1:6],tempstr[6:11],tempstr[11:16], \
                        tempstr[16:21],tempstr[21:26],tempstr[26:],proj.PC, 'J', \
                        proj.bintodec(shifted)))
                    proj.PC = proj.PC + 4
                elif (tempstr[1:6] == '00100'): #BEQ
                    if tempstr[16] == '0':
                        shifted = proj.shifttwo(tempstr[16:])
                        outFileD.write('%s %s %s %s %s %s %s\t%r\t%s\t%s%r, %s%r, #%r\n' \
                        % (tempstr[0],tempstr[1:6],tempstr[6:11],tempstr[11:16], \
                        tempstr[16:21],tempstr[21:26],tempstr[26:],proj.PC, 'BEQ','R', \
                        proj.bintodec(tempstr[6:11]), 'R', proj.bintodec(tempstr[11:16]),\
                        proj.bintodec(shifted)))
                    else:
                        twos = proj.twoscomplement(tempstr[16:])
                        shifted = proj.shifttwo(twos)
                        num = proj.bintodec(shifted) * -1
                        outFileD.write('%s %s %s %s %s %s %s\t%r\t%s\t%s%r, %s%r, #%r\n' \
                        % (tempstr[0],tempstr[1:6],tempstr[6:11],tempstr[11:16], \
                        tempstr[16:21],tempstr[21:26],tempstr[26:],proj.PC, 'BEQ','R', \
                        proj.bintodec(tempstr[6:11]), 'R', proj.bintodec(tempstr[11:16]),\
                        num))
                    proj.PC = proj.PC + 4
                elif ((tempstr[1:6] == '00000') and (tempstr[26:] == '001101')): #BREAK
                    br = True
                    outFileD.write('%s %s %s %s %s %s %s\t%r\t%s\n' \
                        % (tempstr[0],tempstr[1:6],tempstr[6:11],tempstr[11:16], \
                        tempstr[16:21],tempstr[21:26],tempstr[26:],proj.PC, 'BREAK'))
                    proj.PC = proj.PC + 4
                    data_begin = proj.PC
        else:
            if (tempstr[0] == '0'):
                num = proj.bintodec(tempstr)
                proj.memory.append(num)
                outFileD.write('%s\t%r\t%r\n' % (tempstr, proj.PC, num))
                proj.PC = proj.PC + 4
            else:
                twos = proj.twoscomplement(tempstr)
                num = proj.bintodec(twos) * -1
                proj.memory.append(num)
                outFileD.write('%s\t%r\t%r\n' % (tempstr, proj.PC, num))
                proj.PC = proj.PC + 4
        i = i + 1
    outFileD.close()
    data_end = proj.PC    
    #start of simulator
    br = False
    i = 0
    proj.PC = 96
    #simulator phase 1 - read data into structure
    while (i < len(instructions)):
        tempstr = instructions[i]
        if (br == False):
            if (tempstr == ''):
                proj.PC = proj.PC
            elif (tempstr[0] == '0'):
                proj.PC = proj.PC + 4
            else:
                if (tempstr[1:6] == '01000'): #ADDI
                    proj.address.append(proj.PC)
                    proj.instruction.append('ADDI')
                    if tempstr[16] == '0':
                        proj.arg1.append(proj.bintodec(tempstr[11:16]))
                        proj.arg2.append(proj.bintodec(tempstr[6:11]))
                        proj.arg3.append(proj.bintodec(tempstr[16:]))
                    else:
                        twos = proj.twoscomplement(tempstr[16:])
                        num = proj.bintodec(twos) * -1
                        proj.arg1.append(proj.bintodec(tempstr[11:16]))
                        proj.arg2.append(proj.bintodec(tempstr[6:11]))
                        proj.arg3.append(num)                 
                    proj.PC = proj.PC + 4
                elif ((tempstr[1:6] == '00000') and (tempstr[26:] == '100000')): #ADD
                    proj.address.append(proj.PC)
                    proj.instruction.append('ADD')
                    proj.arg1.append(proj.bintodec(tempstr[16:21]))
                    proj.arg2.append(proj.bintodec(tempstr[6:11]))
                    proj.arg3.append(proj.bintodec(tempstr[11:16]))
                    proj.PC = proj.PC + 4
                elif ((tempstr[1:6] == '00000') and (tempstr[26:] == '100010')): #SUB
                    proj.address.append(proj.PC)
                    proj.instruction.append('SUB')
                    proj.arg1.append(proj.bintodec(tempstr[16:21]))
                    proj.arg2.append(proj.bintodec(tempstr[6:11]))
                    proj.arg3.append(proj.bintodec(tempstr[11:16]))
                    proj.PC = proj.PC + 4
                elif ((tempstr[1:6] == '11100') and (tempstr[26:] == '000010')): #MUL
                    proj.address.append(proj.PC)
                    proj.instruction.append('MUL')
                    proj.arg1.append(proj.bintodec(tempstr[16:21]))
                    proj.arg2.append(proj.bintodec(tempstr[6:11]))
                    proj.arg3.append(proj.bintodec(tempstr[11:16]))
                    proj.PC = proj.PC + 4
                elif ((tempstr[1:6] == '00000') and (tempstr[26:] == '100100')): #AND
                    proj.address.append(proj.PC)
                    proj.instruction.append('AND')
                    proj.arg1.append(proj.bintodec(tempstr[16:21]))
                    proj.arg2.append(proj.bintodec(tempstr[6:11]))
                    proj.arg3.append(proj.bintodec(tempstr[11:16]))
                    proj.PC += 4
                elif ((tempstr[1:6] == '00000') and (tempstr[26:] == '100101')): #OR
                    proj.address.append(proj.PC)
                    proj.instruction.append('OR')
                    proj.arg1.append(proj.bintodec(tempstr[16:21]))
                    proj.arg2.append(proj.bintodec(tempstr[6:11]))
                    proj.arg3.append(proj.bintodec(tempstr[11:16]))
                    proj.PC += 4
                elif (tempstr[1:6] == '01011'): #SW
                    proj.address.append(proj.PC)
                    proj.instruction.append('SW')
                    if tempstr[16] == '0':
                        proj.arg1.append(proj.bintodec(tempstr[11:16]))
                        proj.arg2.append(proj.bintodec(tempstr[16:]))
                        proj.arg3.append(proj.bintodec(tempstr[6:11]))
                    else:
                        twos = proj.twoscomplement(tempstr[16:])
                        num = proj.bintodec(twos) * -1
                        proj.arg1.append(proj.bintodec(tempstr[11:16]))
                        proj.arg2.append(num)
                        proj.arg3.append(proj.bintodec(tempstr[6:11]))
                    proj.PC += 4
                elif (tempstr[1:6] == '00011'): #LW
                    proj.address.append(proj.PC)
                    proj.instruction.append('LW')
                    if tempstr[16] == '0':
                        proj.arg1.append(proj.bintodec(tempstr[11:16]))
                        proj.arg2.append(proj.bintodec(tempstr[16:]))
                        proj.arg3.append(proj.bintodec(tempstr[6:11]))
                    else:
                        twos = proj.twoscomplement(tempstr[16:])
                        num = proj.bintodec(twos) * -1
                        proj.arg1.append(proj.bintodec(tempstr[11:16]))
                        proj.arg2.append(num)
                        proj.arg3.append(proj.bintodec(tempstr[6:11]))
                    proj.PC += 4
                elif ((tempstr[1:6] == '00000') and (tempstr[26:] == '001010')): #MOVZ
                    proj.address.append(proj.PC)
                    proj.instruction.append('MOVZ')
                    proj.arg1.append(proj.bintodec(tempstr[16:21]))
                    proj.arg2.append(proj.bintodec(tempstr[6:11]))
                    proj.arg3.append(proj.bintodec(tempstr[11:16]))
                    proj.PC += 4
                elif ((tempstr[1:6] == '00000') and (tempstr[26:] == '000000')): #SLL #NOP
                    if (tempstr[6:26] == '00000000000000000000'):
                        proj.address.append(proj.PC)
                        proj.instruction.append('NOP')
                        proj.arg1.append(proj.bintodec(tempstr[16:21]))
                        proj.arg2.append(proj.bintodec(tempstr[11:16]))
                        proj.arg3.append(proj.bintodec(tempstr[21:26]))
                        proj.PC += 4
                    else:
                        proj.address.append(proj.PC)
                        proj.instruction.append('SLL')
                        proj.arg1.append(proj.bintodec(tempstr[16:21]))
                        proj.arg2.append(proj.bintodec(tempstr[11:16]))
                        proj.arg3.append(proj.bintodec(tempstr[21:26]))
                        proj.PC += 4
                elif ((tempstr[1:6] == '00000') and (tempstr[26:] == '000010')): #SRL
                    proj.address.append(proj.PC)
                    proj.instruction.append('SRL')
                    proj.arg1.append(proj.bintodec(tempstr[16:21]))
                    proj.arg2.append(proj.bintodec(tempstr[11:16]))
                    proj.arg3.append(proj.bintodec(tempstr[21:26]))
                    proj.PC += 4
                elif (tempstr[1:6] == '00100'): #BEQ
                    proj.address.append(proj.PC)
                    proj.instruction.append('BEQ')
                    proj.arg1.append(proj.bintodec(tempstr[6:11])) #NEED TO FINISH
                    if tempstr[16] == '0':
                        shifted = proj.shifttwo(tempstr[16:])
                        outFileD.write('%s %s %s %s %s %s %s\t%r\t%s\t%s%r, %s%r, #%r\n' \
                        % (tempstr[0],tempstr[1:6],tempstr[6:11],tempstr[11:16], \
                        tempstr[16:21],tempstr[21:26],tempstr[26:],proj.PC, 'BEQ','R', \
                        proj.bintodec(tempstr[6:11]), 'R', proj.bintodec(tempstr[11:16]),\
                        proj.bintodec(shifted)))
                    else:
                        twos = proj.twoscomplement(tempstr[16:])
                        shifted = proj.shifttwo(twos)
                        num = proj.bintodec(shifted) * -1
                        outFileD.write('%s %s %s %s %s %s %s\t%r\t%s\t%s%r, %s%r, #%r\n' \
                        % (tempstr[0],tempstr[1:6],tempstr[6:11],tempstr[11:16], \
                        tempstr[16:21],tempstr[21:26],tempstr[26:],proj.PC, 'BEQ','R', \
                        proj.bintodec(tempstr[6:11]), 'R', proj.bintodec(tempstr[11:16]),\
                        num))
                    proj.PC += 4
                elif ((tempstr[1:6] == '00000') and (tempstr[26:] == '001101')): #BREAK
                    br = True
                    proj.address.append(proj.PC)
                    proj.instruction.append('BREAK')
        i = i + 1
    #simulator phase 2 - write the info to simulator text file
    br = False
    i = 0
    row_begin = '===================='    
    while (i < len(proj.instruction) and (br == False)):
        if (proj.instruction[i] == 'ADDI'): #ADDI
            outFileS.write('%s\n' % row_begin)
            outFileS.write('cycle: %r\t%r\t%s\tR%r,R%r,#%r\n\n' % (proj.cycle, \
                proj.address[i], proj.instruction[i], proj.arg1[i], proj.arg2[i], \
                proj.arg3[i]))
            proj.R[proj.arg1[i]] = proj.arg3[i] + proj.R[proj.arg2[i]] #ADDI
        elif (proj.instruction[i] == 'SW'): #SW
            outFileS.write('%s\n' % row_begin)
            outFileS.write('cycle: %r\t%r\t%s\tR%r,%r(R%r)\n\n' % (proj.cycle, \
                proj.address[i], proj.instruction[i], proj.arg1[i], proj.arg2[i], \
                proj.arg3[i]))
            num = ((proj.arg2[i]+proj.R[proj.arg3[i]]-data_begin)/4)
            proj.memory[num] = proj.R[proj.arg1[i]] #SW
        elif (proj.instruction[i] == 'LW'): #LW
            outFileS.write('%s\n' % row_begin)
            outFileS.write('cycle: %r\t%r\t%s\tR%r,%r(R%r)\n\n' % (proj.cycle, \
                proj.address[i], proj.instruction[i], proj.arg1[i], proj.arg2[i], \
                proj.arg3[i]))
            num = ((proj.arg2[i]+proj.R[proj.arg3[i]]-data_begin)/4)
            proj.R[proj.arg1[i]] = proj.memory[num] #LW
        elif (proj.instruction[i] == 'ADD'):#ADD
            outFileS.write('%s\n' % row_begin)
            outFileS.write('cycle: %r\t%r\t%s \tR%r,R%r,R%r\n\n' % (proj.cycle, \
                proj.address[i], proj.instruction[i], proj.arg1[i], proj.arg2[i], \
                proj.arg3[i]))
            proj.R[proj.arg1[i]] = proj.R[proj.arg2[i]] + proj.R[proj.arg3[i]] #ADD
        elif (proj.instruction[i] == 'SUB'):#SUB
            outFileS.write('%s\n' % row_begin)
            outFileS.write('cycle: %r\t%r\t%s \tR%r,R%r,R%r\n\n' % (proj.cycle, \
                proj.address[i], proj.instruction[i], proj.arg1[i], proj.arg2[i], \
                proj.arg3[i]))
            proj.R[proj.arg1[i]] = proj.R[proj.arg2[i]] - proj.R[proj.arg3[i]] #SUB
        elif (proj.instruction[i] == 'MUL'):#MUL
            outFileS.write('%s\n' % row_begin)
            outFileS.write('cycle: %r\t%r\t%s \tR%r,R%r,R%r\n\n' % (proj.cycle, \
                proj.address[i], proj.instruction[i], proj.arg1[i], proj.arg2[i], \
                proj.arg3[i]))
            proj.R[proj.arg1[i]] = proj.R[proj.arg2[i]] * proj.R[proj.arg3[i]] #MUL
        elif (proj.instruction[i] == 'AND'): #AND
            outFileS.write('%s\n' % row_begin)
            outFileS.write('cycle: %r\t%r\t%s \tR%r,R%r,R%r\n\n' % (proj.cycle, \
                proj.address[i], proj.instruction[i], proj.arg1[i], \
                proj.arg2[i], proj.arg3[i]))
            binStr1 = bin(proj.R[proj.arg2[i]])
            binStr2 = bin(proj.R[proj.arg3[i]])
            binNum1 = int(binStr1[2:],2)
            binNum2 = int(binStr2[2:],2)
            proj.R[proj.arg1[i]] = (binNum1 & binNum2) #OR
        elif (proj.instruction[i] == 'OR'): #OR
            outFileS.write('%s\n' % row_begin)
            outFileS.write('cycle: %r\t%r\t%s \tR%r,R%r,R%r\n\n' % (proj.cycle, \
                proj.address[i], proj.instruction[i], proj.arg1[i], \
                proj.arg2[i], proj.arg3[i]))
            binStr1 = bin(proj.R[proj.arg2[i]])
            binStr2 = bin(proj.R[proj.arg3[i]])
            binNum1 = int(binStr1[2:],2)
            binNum2 = int(binStr2[2:],2)
            proj.R[proj.arg1[i]] = (binNum1 | binNum2) #OR
        elif (proj.instruction[i] == 'MOVZ'): #MOVZ
            outFileS.write('%s\n' % row_begin)
            outFileS.write('cycle: %r\t%r\t%s \tR%r,R%r,R%r\n\n' % (proj.cycle, \
                proj.address[i], proj.instruction[i], proj.arg1[i], proj.arg2[i],\
                proj.arg3[i]))
            if (proj.R[proj.arg3[i]] == 0): #MOVZ
                proj.R[proj.arg1[i]] = proj.R[proj.arg2[i]]
        elif (proj.instruction[i] == 'SLL'): #SLL
            outFileS.write('%s\n' % row_begin)
            outFileS.write('cycle: %r\t%r\t%s \tR%r,R%r,#%r\n\n' % (proj.cycle, \
                proj.address[i], proj.instruction[i], proj.arg1[i], proj.arg2[i],\
                proj.arg3[i]))
            proj.R[proj.arg1[i]] = proj.R[proj.arg2[i]] << proj.arg3[i] #SLL
        elif (proj.instruction[i] == 'SRL'): #SRL
            outFileS.write('%s\n' % row_begin)
            outFileS.write('cycle: %r\t%r\t%s \tR%r,R%r,#%r\n\n' % (proj.cycle, \
                proj.address[i], proj.instruction[i], proj.arg1[i], proj.arg2[i],\
                proj.arg3[i]))
            proj.R[proj.arg1[i]] = proj.R[proj.arg2[i]] >> proj.arg3[i] #SRL
        elif (proj.instruction[i] == 'NOP'): #NOP
            outFileS.write('%s\n' % row_begin)
            outFileS.write('cycle: %r\t%r\t%s\n\n' % (proj.cycle, proj.address[i], \
                proj.instruction[i]))
        elif (proj.instruction[i] == 'BREAK'): #BREAK
            br = True
            outFileS.write('%s\n' % row_begin)
            outFileS.write('cycle: %r\t%r\t%s\n\n' % (proj.cycle, proj.address[i], \
                proj.instruction[i]))
        outFileS.write('registers:\n')
        outFileS.write('r00:\t%r\t%r\t%r\t%r\t%r\t%r\t%r\t%r\n' % (proj.R[0], \
            proj.R[1], proj.R[2], proj.R[3], proj.R[4], proj.R[5], proj.R[6], \
            proj.R[7]))
        outFileS.write('r08:\t%r\t%r\t%r\t%r\t%r\t%r\t%r\t%r\n' % (proj.R[8], \
            proj.R[9], proj.R[10], proj.R[11], proj.R[12], proj.R[13], \
            proj.R[14], proj.R[15]))
        outFileS.write('r16:\t%r\t%r\t%r\t%r\t%r\t%r\t%r\t%r\n' % (proj.R[16], \
            proj.R[17], proj.R[18], proj.R[19], proj.R[20], proj.R[21], \
            proj.R[22], proj.R[23]))
        outFileS.write('r24:\t%r\t%r\t%r\t%r\t%r\t%r\t%r\t%r\n\n' % (proj.R[24], \
            proj.R[25], proj.R[26], proj.R[27], proj.R[28], proj.R[29], \
            proj.R[30], proj.R[31]))
        outFileS.write('data:\n')
        j = 0
        data_loop = data_begin
        while (j < (len(proj.memory))):
            if (j == 0):
                outFileS.write('%r:' % data_loop)
            if ((j == 8) or (j == 16) or (j == 24)):
                data_loop += 32 
                outFileS.write('\n%r:' % data_loop)
            outFileS.write('\t%r' % (proj.memory[j]))
            j += 1
        outFileS.write('\n')
        proj.cycle += 1
        i = i + 1
    outFileS.close()
	
if __name__ == '__main__':
    main()