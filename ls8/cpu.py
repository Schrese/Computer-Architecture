"""CPU functionality."""

import sys

# 

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # pass
        self.properties = [0] * 256
        self.gpr = [0] * 8
        self.pc = 0
        # self.ir --> possibly to be used later
        # self.mar --> possibly to be used later
        # self.mdr --> possibly to be used later
        # self.fl --> possibly to be used later

    def ram_read(self, MAR):
        answer = self.properties[MAR]
        print(answer)
        return answer

    def ram_write(self, MAR, MDR):
        self.properties[MAR] = MDR
        

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.properties[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
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
        IR = self.ram_read(self.pc)
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)

        if IR == 0b10000010:
            print('hello')
            self.pc += 2
        elif IR == 0b01000111:
            print('interesting')
            self.pc += 1
        elif IR == 0b00000001:
            print('ohhhhh myyyyyyyy')
            return
        else:
            print('what do?')

