from mcp.server import Server
import mcp.types as types

import aiohttp
import asyncio
from typing import List, Dict, Any

server = Server("multi-tool-orchestrator")

class ToolOrchestrator:
    def __init__(self):
        self.workflows = {
            "morning_briefing": [
                {"tool": "get_calendar_events", "params": {"days": 1}},
                {"tool": "check_github_notifications", "params": {}},
                {"tool": "get_weather", "params": {}},
                {"tool": "check_ci_status", "params": {"repos": ["main-project"]}}
            ],
            "deploy_checklist": [
                {"tool": "run_tests", "params": {"suite": "all"}},
                {"tool": "check_code_coverage", "params": {"threshold": 80}},
                {"tool": "lint_code", "params": {}},
                {"tool": "check_dependencies", "params": {"security": True}},
                {"tool": "generate_changelog", "params": {}}
            ],
            "research_assistant": [
                {"tool": "search_arxiv", "params": {"query": "{query}", "limit": 5}},
                {"tool": "summarize_papers", "params": {"papers": "{arxiv_results}"}},
                {"tool": "find_implementations", "params": {"papers": "{arxiv_results}"}},
                {"tool": "create_reading_list", "params": {"summaries": "{summaries}"}}
            ]
        }

    async def execute_workflow(self, workflow_name: str, context: Dict[str, Any] = {}):
        if workflow_name not in self.workflows:
            raise ValueError(f"Unknown workflow: {workflow_name}")

        workflow = self.workflows[workflow_name]
        results = {}

        for step in workflow:
            # Replace placeholders in parameters
            params = {}
            for key, value in step["params"].items():
                if isinstance(value, str) and value.startswith("{") and value.endswith("}"):
                    param_name = value[1:-1]
                    if param_name in context:
                        params[key] = context[param_name]
                    elif param_name in results:
                        params[key] = results[param_name]
                else:
                    params[key] = value

            # Execute tool
            result = await self.execute_tool(step["tool"], params)
            results[step["tool"]] = result

        return results

    async def execute_tool(self, tool_name: str, params: Dict[str, Any]):
        # Tool implementations would go here
        # This is a simplified example
        if tool_name == "get_weather":
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://api.weather.com/...") as resp:
                    return await resp.json()
        # ... implement other tools

        return f"Executed {tool_name} with {params}"

orchestrator = ToolOrchestrator()

@server.list_tools()
async def handle_list_tools():
    return [
        types.Tool(
            name="execute_workflow",
            description="Execute a predefined workflow",
            inputSchema={
                "type": "object",
                "properties": {
                    "workflow": {
                        "type": "string",
                        "enum": ["morning_briefing", "deploy_checklist", "research_assistant"]
                    },
                    "context": {"type": "object"}
                },
                "required": ["workflow"]
            }
        ),
        types.Tool(
            name="create_custom_workflow",
            description="Create a custom workflow",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "steps": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "tool": {"type": "string"},
                                "params": {"type": "object"}
                            }
                        }
                    }
                },
                "required": ["name", "steps"]
            }
        )
    ]
@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    """
    Handle tool calls and return results as an iterable of TextContent.
    """
    if name == "execute_workflow":
        result = await orchestrator.execute_workflow(
            arguments["workflow"],
            arguments.get("context", {})
        )
        # Convert dict result to a readable string
        text = f"Workflow '{arguments['workflow']}' executed. Results: {result}"
        return [types.TextContent(type="text", text=text)]
    elif name == "create_custom_workflow":
        orchestrator.workflows[arguments["name"]] = arguments["steps"]
        text = f"Created workflow: {arguments['name']}"
        return [types.TextContent(type="text", text=text)]
    else:
        return [types.TextContent(type="text", text=f"Unknown tool: {name}")]
