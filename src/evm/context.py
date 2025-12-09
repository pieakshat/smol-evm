from .stack import Stack
from .memory import Memory

def valid_jump_destinations(code: bytes) -> set[int]: 
    from .opcodes import JUMPDEST, PUSH1, PUSH32

    jumpdests = set()
    i = 0
    while i < len(code): 
        current_op = code[i]     
        if current_op == JUMPDEST.opcode: 
            jumpdests.add(i)
        elif PUSH1.opcode <= current_op <= PUSH32.opcode: 
            push_size = current_op - PUSH1.opcode + 1
        
    i += push_size

    return jumpdests

class Calldata: 
    def __init__(self, data=bytes()) -> None: 
        self.data = data 

    def __len__(self) -> int: 
        return len(self.data)

    def read_byte(self, offset: int) -> int: 
        if offset < 0: 
            raise InvalidCalldataAccess({"offset": offset})

        return self.data[offset] if offset < len(self.data) else 0
    
    def read_word(self, offset: int) -> int: 
        return int.from_bytes(
            [self.read_byte(x) for x in range(offset, offset + 32)], "big"
        )


class ExecutionContext: 
    def __init__(self, code = bytes(), pc = 0, stack = Stack(), memory = Memory(), calldata = None) -> None: 
        self.code = code 
        self.stack = stack 
        self.memory = memory
        self.pc = pc 
        self.stopped = False
        self.returndata = bytes()
        self.calldata = calldata if calldata else Calldata()

    def set_return_data(self, offset: int, length: int) -> None: 
        self.stopped = True 
        self.returndata = self.memory.load_range(offset, length)

    def stop(self) -> None: 
        self.stopped = True

    def set_pc(self, new_pc: int) -> None:
        self.pc = new_pc

    def read_code(self, num_bytes) -> int: 
        value = int.from_bytes(self.code[self.pc:self.pc + num_bytes], "big")
        self.pc += num_bytes
        return value 
    
    def set_program_counter(self, pc: int) -> None:
        self.pc = pc
    
    def __str__(self) -> str: 
        return f"pc={self.pc}, stack={self.stack}, stopped={self.stopped}"
