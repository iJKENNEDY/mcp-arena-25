from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Demo")

# add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """add two numbers"""
    return a + b

@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    return f"Hello, {name}"

