from .context import ExecutionContext
from .opcodes import decode_opcode

class ExecutionLimitReached(Exception):
    pass

def run(code: bytes, max_steps: int = None, verbose: bool = False) -> bytes: 
    context = ExecutionContext(code=code)
    steps = 0

    while not context.stopped: 
        if max_steps is not None and steps >= max_steps:
            raise ExecutionLimitReached(f"Execution limit of {max_steps} steps reached")
        
        pc_before = context.pc
        instruction = decode_opcode(context) 
        instruction.execute(context)
        steps += 1

        if verbose:
            print(f"{instruction} @ pc={pc_before}" )
            print(context) 
            print() 

    if verbose:
        print(f"Output: 0x{context.returndata.hex()}")
    
    return context.returndata