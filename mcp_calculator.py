from mcp.server.fastmcp import FastMCP
from typing import Optional

# Initialize FastMCP server
mcp = FastMCP("Calculator")

@mcp.tool()
def calculate(
    expression: Optional[str] = None, 
    number1: Optional[float] = None, 
    operation: Optional[str] = None, 
    number2: Optional[float] = None
) -> str:
    """
    Evaluates a mathematical expression and returns the result.
    Supports two formats:
    1. A single string 'expression' (e.g., '1 + 1')
    2. Separate 'number1', 'operation', and 'number2' (e.g., 1, '+', 1)
    """
    try:
        # Format 1: Single expression string
        if expression is not None:
            result = eval(str(expression), {"__builtins__": None}, {})
            return str(result)
        
        # Format 2: Separate parts
        if number1 is not None and operation is not None and number2 is not None:
            expr = f"{number1} {operation} {number2}"
            result = eval(expr, {"__builtins__": None}, {})
            return str(result)
            
        return "Error: Please provide either an 'expression' string or 'number1', 'operation', and 'number2'."
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    mcp.run()
