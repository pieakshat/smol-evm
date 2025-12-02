from .execution import ExecutionContext 

INSTRUCTIONS = [] 
INSTRUCTIONS_BY_OPCODE = {}

class Instruction: 
    def __init__(self, opcode: int, name: str): 
        self.opcode = opcode
        self.name = name 

    def execute(self, context: ExecutionContext) -> None: 
        raise NotImplementedError

    def register_instruction(opcode: int, name: str, execute_func: callable):
        instruction = Instruction(opcode, name)
        instruction.execute = execute_func
        INSTRUCTIONS.append(instruction) 

        assert opcode not in INSTRUCTIONS_BY_OPCODE 
        INSTRUCTIONS_BY_OPCODE[opcode] = instruction

        return instruction