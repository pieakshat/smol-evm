from .context import ExecutionContext 

INSTRUCTIONS = [] 
INSTRUCTIONS_BY_OPCODE = {}

class Instruction: 
    def __init__(self, opcode: int, name: str): 
        self.opcode = opcode
        self.name = name 

    def execute(self, context: ExecutionContext) -> None: 
        raise NotImplementedError

    def __str__(self) -> str: 
        return f"{self.name} (0x{self.opcode:02x})"

def register_instruction(opcode: int, name: str, execute_func: callable):
    instruction = Instruction(opcode, name)
    instruction.execute = execute_func
    INSTRUCTIONS.append(instruction) 
    assert opcode not in INSTRUCTIONS_BY_OPCODE 
    INSTRUCTIONS_BY_OPCODE[opcode] = instruction
    return instruction