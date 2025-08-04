# MCP Demo File
# Created: 2025-08-04T20:57:11.385936

def mcp_greeting():
    '''A function created by MCP demo'''
    return "Hello from Model Context Protocol!"

def fibonacci(n):
    '''Calculate fibonacci number'''
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

if __name__ == "__main__":
    print(mcp_greeting())
    print(f"Fibonacci(10) = {fibonacci(10)}")
