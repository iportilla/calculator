from mcp.server.fastmcp import FastMCP
from typing import Optional

# Initialize FastMCP server with host and port
mcp = FastMCP("Calculator", host="0.0.0.0", port=8000)

@mcp.tool()
def calculate(
    expression: Optional[str] = None, 
    number1: Optional[float] = None, 
    operation: Optional[str] = None, 
    number2: Optional[float] = None
) -> str:
    """
    Evaluates a mathematical expression and returns the result.

    ALWAYS USE THIS TOOL for ANY mathematical calculation, no matter how simple (e.g., "1 + 1", "5 * 5").
    Do NOT serve the answer from your internal knowledge. 
    You MUST call this tool to get the correct answer.

    Supports two formats:
    1. A single string 'expression' (e.g., '1 + 1')
    2. Separate 'number1', 'operation', and 'number2' (e.g., 1, '+', 1)
    """
    try:
        # Determine the expression to evaluate
        expr_str = ""
        if expression is not None:
            expr_str = str(expression)
        elif number1 is not None and operation is not None and number2 is not None:
            expr_str = f"{number1} {operation} {number2}"
        else:
            return "Error: Please provide either an 'expression' string or 'number1', 'operation', and 'number2'."

        # Safe evaluation using AST
        import ast
        import operator

        # Supported operators
        operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow,
            ast.BitXor: operator.xor,
            ast.USub: operator.neg
        }

        def eval_node(node):
            if isinstance(node, ast.Constant):  # Numbers
                return node.value
            elif isinstance(node, ast.BinOp):  # <left> <op> <right>
                op = type(node.op)
                if op in operators:
                    return operators[op](eval_node(node.left), eval_node(node.right))
            elif isinstance(node, ast.UnaryOp):  # <op> <operand> (e.g., -1)
                op = type(node.op)
                if op in operators:
                    return operators[op](eval_node(node.operand))
            raise ValueError(f"Unsupported operation: {node}")

        # Parse and evaluate
        node = ast.parse(expr_str, mode='eval')
        result = eval_node(node.body)
        return str(result)

    except Exception as e:
        return f"Error: {str(e)}"

import sys

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "sse":
        mcp.run(transport="sse")
    else:
        mcp.run()
