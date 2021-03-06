# MDR = Memory Data Register
# MAR = Memory Address Register

import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
ADD = 0b10100000

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        pass
        self.pc = 0
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.SP = 0xf3
        

    def load(self, filename):
        """Load a program into memory."""
        # print("Loading CPU...")
        address = 0

        try:
            address = 0
            #open file
            with open(sys.argv[1]) as f:
                #read all line
                for line in f:
                    # make sure no errors occur in spacing
                    comment_split = line.strip().split("#")
                    # number string to int
                    value = comment_split[0].strip()
                    # Leave empty
                    if value == "":
                        continue
                    instruction = int(value, 2)
                    # Populate array
                    self.ram[address] = instruction
                    address += 1

        except:
            print("cant find file")
            sys.exit(2)


    def ram_read(self, address):
        # The MAR contains address being read or written to.
        return self.ram[address]

    def ram_write(self, address, value):
        # The MDR contains data that was read or data to be written. 
        self.ram[address] = value


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == MUL:
            self.reg[reg_a] *= self.reg[reg_b]
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
        while True:
            ops = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            # print(IR, self.pc, operand_a, operand_b)
            if ops == LDI:
                self.reg[operand_a] = operand_b
                # print(self.pc, self.reg, self.ram)
                self.pc += 3
            elif ops == PRN:
                print(self.reg[operand_a])
                self.pc += 2
            elif ops == MUL:
                self.alu(ops, operand_a, operand_b)
                self.pc += 3
            elif ops == PUSH:
                operand_a = self.ram_read(self.pc + 1) 
                self.ram_write(self.SP, self.reg[operand_a])
                self.pc += 2
                self.SP -= 1
            elif ops == POP:
                operand_a = self.ram_read(self.pc + 1)
                self.reg[operand_a] = self.ram_read(self.SP+1)
                self.SP += 1
                self.pc += 2
            elif ops == CALL:
                    # print(operand_a)
                operand_a = self.ram_read(self.pc + 1)
                self.SP -= 1
                self.ram_write(self.SP, self.pc + 2)
                self.pc = self.reg[operand_a]
                # print(self.pc)
            elif ops == RET:
                self.pc = self.ram_read(self.SP)
                self.SP += 1
            elif ops == ADD:
                self.pc +=3
                self.alu("ADD", operand_a, operand_b)        
            elif ops == HLT:
                sys.exit(0)
            else:
                print(f"Did not work")
                sys.exit(1)