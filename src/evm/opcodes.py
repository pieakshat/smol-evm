from .instruction import register_instruction
from .context import ExecutionContext
from .instruction import Instruction, INSTRUCTIONS_BY_OPCODE
from typing import Sequence, Union

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
MSTORE8 = register_instruction(
    0x53, 
    "MSTORE8", 
    (lambda ctx: ctx.memory.store(ctx.stack.pop(), ctx.stack.pop() % 256)), 
)
RETURN = register_instruction(
    0xf3, 
    "RETURN", 
    (lambda ctx: ctx.set_return_data(ctx.stack.pop(), ctx.stack.pop())), 
)
JUMPDEST = register_instruction(
    0x5B, 
    "JUMPDEST", 
    (lambda ctx: ctx), 
)

JUMP = register_instruction(
    0x56,
    "JUMP",
    (lambda ctx: ctx.set_pc(ctx.stack.pop())),
)

JUMPI = register_instruction(
    0x57, 
    "JUMPI", 
    (lambda ctx: execute_JUMPI(ctx)),
)

PUSH32 = register_instruction(0x7f, "PUSH32", (lambda ctx: ctx.stack.push(ctx.read_code(32))))
DUP1 = register_instruction(0x80, "DUP1", (lambda ctx: ctx.stack.push(ctx.stack.peek(0))))
DUP2 = register_instruction(0x81, "DUP2", (lambda ctx: ctx.stack.push(ctx.stack.peek(1))))
DUP3 = register_instruction(0x82, "DUP3", (lambda ctx: ctx.stack.push(ctx.stack.peek(2))))
SWAP1 = register_instruction(0x90, "SWAP1", (lambda ctx: ctx.stack.swap(1)))
SUB = register_instruction(
    0x03,
    "SUB",
    (lambda ctx: (lambda a, b: ctx.stack.push((a - b) % 2**256))(ctx.stack.pop(), ctx.stack.pop())),
)


def decode_opcode(context: ExecutionContext) -> Instruction: 
    if context.pc < 0 or context.pc >= len(context.code): 
        raise InvalidCodeOffset({"code": context.code, "pc": context.pc})
    
    opcode = context.read_code(1)
    instruction = INSTRUCTIONS_BY_OPCODE.get(opcode)

    if instruction is None: 
        raise UnknownOpcode({"opcode": opcode})
    
    return instruction 

def assemble(instructions: Sequence[Union[Instruction, int]], print_bin=True) -> bytes: 
    result = bytes() 
    for item in instructions: 
        if isinstance(item, Instruction): 
            result += bytes([item.opcode]) 
        elif isinstance(item, int):
            result += int_to_bytes(item) 
        else: 
            raise TypeError(f"Unexpected {type(item)} in {instructions}")
    
    if print_bin: 
        print(result.hex())
    
    return result

        
def int_to_bytes(x: int) -> bytes: 
    return x.to_bytes(max(1, ((x.bit_length()) + 7) // 8), "big") 

def execute_JUMPI(ctx: ExecutionContext): 
    target_pc = ctx.stack.pop()
    cond = ctx.stack.pop()
    if cond != 0:  
        ctx.set_pc(target_pc)



class InvalidCodeOffset(Exception): 
    ... 

class UnknownOpcode(Exception): 
    ... 

class InvalidJumpDestination(Exception): 
    ... 
