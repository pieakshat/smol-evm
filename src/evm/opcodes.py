from .instruction import register_instruction

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