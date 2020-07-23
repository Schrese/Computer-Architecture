"""CPU functionality."""

import sys

# 
LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MULT = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
ADD = 0b10100000

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # pass
        self.properties = [0] * 256
        self.reg = [0] * 8 # reg = general purpose registers
        self.pc = 0 # ---> program counter
        self.sp = 0xF4 # --> Stack Pointer
        self.ir = 0

    def ram_read(self, MAR):
        answer = self.properties[MAR]
        # print(answer)
        return answer

    def ram_write(self, MAR, MDR):
        self.properties[MAR] = MDR
        return
        

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.properties[address] = instruction
        #     address += 1

        # with open('examples/print8.ls8', 'r') as f:
        # self.trace()
        if len(sys.argv) != 2:
            print("usage: python3 ls8.py examples/filename")
            sys.exit(1)
        # print(sys.argv[1])
        try:
            with open(sys.argv[1]) as f:
                for instruction in f:
                    try:
                        instruction = instruction.split("#", 1)[0]
                        instruction = int(instruction, 2)
                        self.properties[address] = instruction
                        address += 1
                    except ValueError: 
                        pass
        except FileNotFoundError:
            print(f"Couldn't find file {sys.argv[1]}")
            sys.exit(1)


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
            # print(self.reg[reg_a])
        #elif op == "SUB": etc
        elif op == "MULT":
            self.reg[reg_a] *= self.reg[reg_b]
            # print(self.reg[reg_a])
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        # pass
        self.trace()
        cont = True

        while cont:
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if IR == LDI: #LDI
                # print('hello')
                self.LDI_Handler(operand_a, operand_b)
                self.pc += 3
            elif IR == PRN: # PRN
                # print('interesting')
                self.PRN_Handler(operand_a)
                self.pc += 2
            elif IR == ADD: # ADD
                self.alu("ADD", operand_a, operand_b)
                self.pc += 3
            elif IR == MULT: # MULT
                self.alu("MULT", operand_a, operand_b)
                # self.MULT_Handler(operand_a, operand_b)
                self.pc += 3
            elif IR == PUSH:
                # self.sp -=1 # Moves the pointer down/decrements it
                registry_address = self.ram_read(self.pc + 1)
                self.PUSH_Handler(self.reg[registry_address])
                # self.ram_write(self.sp, self.reg[registry_address])
                self.pc += 2
            elif IR == POP:
                value = self.POP_Handler()
                registry_address = self.ram_read(self.pc + 1)
                self.reg[registry_address] = value
                self.pc += 2
            elif IR == CALL:
                # pass
                # print('made it to call')
                self.reg[7] -= 1 # ---> stack pointer wasn't pointing at the right place, but only for this function. 
                self.PUSH_Handler(self.pc + 2)

                reg_num = self.properties[self.pc + 1]
                subroutine_addr = self.reg[reg_num]

                self.pc = subroutine_addr

            elif IR == RET:
                # pass
                value = self.POP_Handler()
                registry_address = self.ram_read(self.pc + 1)
                self.reg[registry_address] = value
                self.pc = value
            elif IR == HLT:
                # print('ohhhhh myyyyyyyy')
                cont = False
                # sys.exit(1)
                # return
            else:
                print('what do?')
            # print(self.pc, self.sp, "I'm PC Bro!")

    # Set the value of a register to an integer.
    def LDI_Handler(self, key, value):
        self.reg[key] = value
        # print(value, 'coming from here')
        
    # Print numeric value stored in the given register.
    def PRN_Handler(self, value):
        print(self.reg[value])

    # def MULT_Handler(self, val1, val2):
    #     total = val1 * val2
    #     self.reg[val1] *= self.reg[val2]
    #     print(self.reg[val1], 'total')
    #     # return total
    def PUSH_Handler(self, v):
        self.sp -=1 
        self.ram_write(self.sp, v)
        # self.pc += 2

    def POP_Handler(self):
        if self.sp < 0xF4:
            value = self.ram_read(self.sp)
            self.sp += 1
            return value
        else:
            print("Error: stack is empty")
            cont = False    

    def CALL_Handler(self):
        pass

    def RET_Handler(self):
        pass