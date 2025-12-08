from evm.opcodes import JUMPDEST, PUSH1, JUMP, assemble
from evm.runner import run, ExecutionLimitReached
import pytest

def test_infinite_loop(): 

    code = assemble([
        JUMPDEST, 
        PUSH1, 0, 
        JUMP
    ])
    with pytest.raises(ExecutionLimitReached): 
        run(code, max_steps=100)