class ExecutionContext: 
    def __init__(self, code = bytes(), pc = 0, stack = Stack(), memory = Memory()) -> None: 
        self.code = code 
        self.stack = stack 
        self.memory = memory
        self.pc = pc 
        self.stopped = False

    def stop(self) -> None: 
        self.stopped = True

    def read_code(self, num_bytes) -> int: 
        value = int.from_bytes(self.code[self.pc:self.pc + num_bytes], "big")
        self.pc += num_bytes
        return value 
