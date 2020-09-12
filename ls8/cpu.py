import sys

# Instructions
HLT = 0b00000001
PRN = 0b01000111
LDI = 0b10000010
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101

# Flags
L = 0b00000100
G = 0b00000010
E = 0b00000001

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256 #256 bytes memory
        self.reg = [0] * 8 #8 registers
        self.pc = 0        #program counter----currently executing instuction
        self.running = True #if program is running 
        self.sp = 7
        self.fl = 0


    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value


    if len(sys.argv) != 2:       #If there isn't enough arguments and we crash send error example
        print("Example to Use: ls8.py filename")
        sys.exit(1)               #Exit program if it fails
    
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
        #       self.ram[address] = instruction
        #     address += 1


        # Bringing in dynamic programs
        file = sys.argv[1]           #Open file using command line

        with open(file) as program_file:          #Opening another file
            for line in program_file:             #For every line in program file do something
                program_split = line.split('#')           #Only get the nums of program by converting into array [0]
                # print(program_split)
                program_value = program_split[0].strip()  #remove whitespace from line of program
                # print(program_value)
                if program_value == "":                    #make sure there is value before # in eachline
                    continue

                program_num = int(program_value, 2)           #the num left from strip is usable to add to ram---converts string to number
                # self.ram_write(address, program_num)       # add num from program to the our ram
                self.ram[address] = program_num
                address += 1

            # print(program_num)
            print(self.ram)


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        
        elif op == "CMP":
            if self.reg[reg_a] == self.reg[reg_b]:
                self.fl = E
            if self.reg[reg_a] < self.reg[reg_b]:
                self.fl = L
            if self.reg[reg_a] > self.reg[reg_b]:
                self.fl = G

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

        while self.running:
            instruction = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            
            if instruction == LDI: #store value in register or set register to value
                #register location at pc + 1
                #value is at pc + 2
                self.reg[operand_a] = operand_b
                self.pc += 3

            elif instruction == PRN: #PRN prints numeric value stored in given register
                print(self.reg[operand_a])
                self.pc += 2

            elif instruction == MUL:
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3
            
            # MVP instructions below
            elif instruction == CMP:
                self.alu('CMP', operand_a, operand_b)  #run ALU 

            elif instruction == JMP:
                 self.pc = self.reg[operand_a] #setting program counter to given register

            elif instruction == JEQ:
                if self.fl == E:
                    self.pc = self.reg[operand_a]
                # need an else if they are not equal????
                else:
                    self.pc += 1

            elif instruction == JNE:
                if self.fl != E:
                    self.pc = self.reg[operand_a]
                #else do what?
                else:
                    self.pc += 1



            elif instruction == PUSH:
                value_in_register = self.reg[operand_a]
                self.reg[self.sp] -= 1     #decrement the stack pointer
                self.ram[self.reg[self.sp]] = value_in_register    #write the value of the given registter to memory at the SP location
                self.pc += 2

            elif instruction == POP:
                value_from_memory = self.ram[self.reg[self.sp]]
                self.reg[operand_a] = value_from_memory
                self.reg[self.sp] += 1
                self.pc += 2

            elif instruction == HLT: #stops program running 
                self.running = False
                self.pc += 1


