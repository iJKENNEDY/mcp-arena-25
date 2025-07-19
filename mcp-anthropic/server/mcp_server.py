# mcp_server.py
"""
Servidor MCP101 para la gestión de recursos personales.
Cumple con las convenciones PEP 8, PEP 257 y las reglas del proyecto MCP101.
"""
from typing import List, Dict, Any
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types
from pydantic import AnyUrl, ValidationError

# Initialize the server
server = Server("personal-knowledge-base")

def get_notes() -> str:
    """
    Simula la obtención de notas personales.
    En una implementación real, se leería desde una base de datos o API.
    Returns:
        str: Contenido de las notas personales.
    """
    return "My AI/ML study notes:\n- Transformers are the foundation..."

@server.list_resources()
async def handle_list_resources() -> List[types.Resource]:
    """
    List available resources.
    Returns:
        List[types.Resource]: Lista de recursos disponibles.
    """
    return [
        types.Resource(
            uri=AnyUrl("knowledge://notes"),
            name="Personal Notes",
            description="Access to my markdown notes",
            mimeType="text/plain",
        )
    ]

@server.read_resource()
async def handle_read_resource(uri: AnyUrl) -> str:
    """
    Read a specific resource.
    Args:
        uri (AnyUrl): URI del recurso a leer.
    Returns:
        str: Contenido del recurso.
    Raises:
        ValueError: Si el recurso no es reconocido.
    """
    if str(uri) == "knowledge://notes":
        return get_notes()
    raise ValueError(f"Unknown resource: {uri}")

@server.list_tools()
async def handle_list_tools() -> List[types.Tool]:
    """
    List available tools.
    Returns:
        List[types.Tool]: Lista de herramientas disponibles.
    """
    return [
        types.Tool(
            name="search_notes",
            description="Search through personal notes",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query"
                    }
                },
                "required": ["query"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """
    Execute a tool.
    Args:
        name (str): Nombre de la herramienta.
        arguments (Dict[str, Any]): Argumentos para la herramienta.
    Returns:
        List[types.TextContent]: Resultado de la herramienta.
    Raises:
        ValueError: Si la herramienta no es reconocida.
    """
    if name == "search_notes":
        query = arguments.get("query", "")
        if not query:
            return [types.TextContent(type="text", text="No query provided. Please specify a search term.")]
        return [types.TextContent(type="text", text=f"Found 3 notes matching '{query}'...")]
    raise ValueError(f"Unknown tool: {name}")

async def main() -> None:
    """
    Main entry point for running the server.
    """
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="personal-knowledge-base",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

"""
Example usage:
    $ python mcp_server.py
    # El servidor se inicia y expone los recursos y herramientas definidos.
"""
