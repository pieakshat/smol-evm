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
    
    def peek(self, index: int) -> int:
        """Peek at stack item at given index (0 = top of stack)"""
        if index < 0 or index >= len(self.stack):
            raise StackUnderflow()
        return self.stack[-(index + 1)]
    
    def swap(self, n: int) -> None:
        """Swap the top of stack with the item at position n (1 = swap with second item)"""
        if len(self.stack) < n + 1:
            raise StackUnderflow()
        # Swap stack[-1] with stack[-(n+1)]
        self.stack[-1], self.stack[-(n+1)] = self.stack[-(n+1)], self.stack[-1]
    
    def __str__(self) -> str: 
        return str(self.stack)

class StackOverflow(Exception): 
    ... 

class StackUnderflow(Exception): 
    ... 

class InvalidStackItem(Exception): 
    ... 

