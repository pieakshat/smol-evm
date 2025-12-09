from evm.opcodes import PUSH1, DUP1, DUP2, DUP3, SWAP1, JUMP, JUMPDEST, assemble, JUMPI, RETURN, MSTORE8, ADD, SUB
from evm.runner import run, ExecutionLimitReached

def test_four_squared(): 
    code = assemble([

    # STACK 
    PUSH1, 4, 
    DUP1, 
    PUSH1, 0, 

    # loop condition 
    # if loops != 0, jump to loop_body 
    JUMPDEST, 
    DUP2, 
    PUSH1, 18, 
    JUMPI, 

    # return result 
    PUSH1, 0, 
    MSTORE8, 
    PUSH1, 1, 
    PUSH1, 0, 
    RETURN, 

    JUMPDEST, 

    DUP3, 
    ADD, 

    SWAP1, 
    PUSH1, 1, 
    SWAP1, 
    SUB, 

    SWAP1, 

    PUSH1, 5, 
    JUMP, 
])

    ret = run(code, verbose=True, max_steps=200)
    assert int.from_bytes(ret, 'big') == 4 * 4