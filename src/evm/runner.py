from .context import ExecutionContext
from .opcodes import decode_opcode

class ExecutionLimitReached(Exception):
    pass

def run(
    code: bytes, 
    max_steps: int = None,
    verbose: bool = False, 
    max_steps=0, 
    prehook = None, 
    posthook = None, 
    ) -> bytes: 
    context = ExecutionContext(code=code, calldata = Calldata(calldata))
    steps = 0

    while not context.stopped: 
        if max_steps is not None and steps >= max_steps:
            raise ExecutionLimitReached(f"Execution limit of {max_steps} steps reached")
        
        pc_before = context.pc
        instruction = decode_opcode(context) 

        if prehook: 
            prehook(context, instruction)
        
        instruction.execute(context)

        if posthook: 
            posthook(context, instruction)
            
        steps += 1

        if verbose:
            print(f"{instruction} @ pc={pc_before}" )
            print(context) 
            print() 

    if verbose:
        print(f"Output: 0x{context.returndata.hex()}")
    
    return context.returndata