from .instruction import register_instruction
from .execution import ExecutionContext
from .instruction import Instruction, INSTRUCTIONS_BY_OPCODE

STOP = register_instruction(0x00, "STOP", (lambda ctx: ctx.stop()))
PUSH1 = register_instruction(
    0x60, 
    "PUSH1", 
    (lambda ctx: ctx.stack.push(ctx.read_code(1))), 
)
ADD = register_instruction(
    0x01, 
    "ADD", 
    (lambda ctx: ctx.stack.push((ctx.stack.pop() + ctx.stack.pop()) % 2**256)), 
)
MUL = register_instruction(
    0x02, 
    "MUL", 
    (lambda ctx: ctx.stack.push((ctx.stack.pop() * ctx.stack.pop()) % 2**256)),
)
MSOTRE8 = register_instruction(
    0x53, 
    "MSTORE8", 
    (lambda ctx: ctx.memory.store(ctx.stack.pop(), ctx.stack.pop() % 256)), 
)
RETURN = register_instruction(
    0xf3, 
    "RETURN", 
    (lambda ctx: ctx.set_return_data(ctx.stack.pop(), ctx.stack.pop())), 
) 

def decode_opcode(context: ExecutionContext) -> Instruction: 
    if context.pc < 0 or context.pc >= len(context.code): 
        raise InvalidCodeOffset({"code": context.code, "pc": context.pc})
    
    opcode = context.read_code(1)
    instruction = INSTRUCTIONS_BY_OPCODE.get(opcode)

    if instruction is None: 
        raise UnknownOpcode({"opcode": opcode})
    
    return instruction 

class InvalidCodeOffset(Exception): 
    ... 

class UnknownOpcode(Exception): 
    ... 
