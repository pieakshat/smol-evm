from .constants import MAX_STACK_DEPTH, MAX_UINT256

class Stack: 
    def __init__(self, max_depth=MAX_STACK_DEPTH) -> None:
        self.stack = []
        self.max_depth = max_depth

        def push(self, item: int) -> None: 
            if item < 0 or item >= MAX_UINT256: 
                raise InvalidStackItem("Item:", item) 
            
            if len(self.stack) >= self.max_depth: 
                raise StackOverflow()
            
            self.stack.append(item)

        def pop(self) -> int: 
            if len(self.stack) == 0: 
                raise StackUnderflow()
            
            return self.stack.pop() 

        def __str__(self) -> str: 
            return str(self.stack)
        
        def __repr__(self) -> str: 
            return str(self)
        
class StackOverflow(Exception): 
    ... 

class StackUnderflow(Exception): 
    ... 

class InvalidStackItem(Exception): 
    ... 

