from typing import List, Dict, Any, Optional
from mcp.server import Server
import mcp.types as types
import sqlite3
from datetime import datetime

server = Server("memory-bank")

class MemoryBank:
    """
    Class for storing and recalling user or conversation memories using SQLite.
    """
    def __init__(self) -> None:
        self.conn = sqlite3.connect('memories.db')
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY,
                category TEXT,
                content TEXT,
                importance INTEGER,
                created_at TIMESTAMP,
                accessed_count INTEGER DEFAULT 0
            )
        ''')

    def store_memory(self, category: str, content: str, importance: int = 5) -> None:
        """
        Store a memory in the database.
        Args:
            category (str): Memory category.
            content (str): Memory content.
            importance (int): Importance level (default 5).
        """
        self.conn.execute(
            "INSERT INTO memories (category, content, importance, created_at) VALUES (?, ?, ?, ?)",
            (category, content, importance, datetime.now())
        )
        self.conn.commit()

    def recall_memories(self, category: Optional[str] = None, limit: int = 10) -> List[sqlite3.Row]:
        """
        Recall memories from the database, optionally filtered by category.
        Args:
            category (Optional[str]): Category to filter by.
            limit (int): Maximum number of memories to return.
        Returns:
            List[sqlite3.Row]: List of memory rows.
        """
        query = "SELECT * FROM memories"
        params = []
        if category:
            query += " WHERE category = ?"
            params.append(category)
        query += " ORDER BY importance DESC, accessed_count DESC LIMIT ?"
        params.append(limit)
        return self.conn.execute(query, params).fetchall()

memory_bank = MemoryBank()

@server.list_tools()
async def handle_list_tools() -> List[types.Tool]:
    """
    List available tools for memory bank operations.
    Returns:
        List[types.Tool]: List of tool definitions.
    """
    return [
        types.Tool(
            name="remember",
            description="Store a memory about the user or conversation",
            inputSchema={
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "enum": ["preference", "personal_info", "project", "idea", "goal"]
                    },
                    "content": {"type": "string"},
                    "importance": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 10
                    }
                },
                "required": ["category", "content"]
            }
        ),
        types.Tool(
            name="recall",
            description="Recall memories from the memory bank",
            inputSchema={
                "type": "object",
                "properties": {
                    "category": {"type": "string"},
                    "limit": {"type": "integer", "default": 10}
                }
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> Any:
    """
    Execute a tool operation for the memory bank.
    Args:
        name (str): Tool name.
        arguments (Dict[str, Any]): Tool arguments.
    Returns:
        Any: Result of the tool operation.
    Raises:
        ValueError: If the tool name is unknown.
    """
    if name == "remember":
        try:
            memory_bank.store_memory(
                arguments["category"],
                arguments["content"],
                arguments.get("importance", 5)
            )
            return f"Stored memory in {arguments['category']} category"
        except Exception as e:
            return f"Error storing memory: {e}"
    elif name == "recall":
        try:
            memories = memory_bank.recall_memories(
                arguments.get("category"),
                arguments.get("limit", 10)
            )
            return {
                "memories": [
                    {
                        "category": m[1],
                        "content": m[2],
                        "importance": m[3],
                        "created": m[4]
                    }
                    for m in memories
                ]
            }
        except Exception as e:
            return {"error": f"Error recalling memories: {e}"}
    raise ValueError(f"Unknown tool: {name}")

# Example usage:
# result = memory_bank.store_memory("project", "Finish MCP101", 8)
# memories = memory_bank.recall_memories("project", 5)
