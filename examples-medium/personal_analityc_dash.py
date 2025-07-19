# personal analytics dashboard
"""
Personal Analytics Dashboard using MCP tools.
Follows PEP 8, PEP 257, and MCP project standards.
"""
import mcp.types as types
from mcp.server import Server
from pathlib import Path
from typing import List, Dict, Any
import json
from datetime import datetime, timedelta
from collections import defaultdict

server = Server("personal-analytics-dashboard")

class ProductivityTracker:
    """
    Tracks coding sessions and provides productivity insights.
    """
    def __init__(self) -> None:
        self.data_file = Path.home() / '.mcp' / 'productivity.json'
        self.data_file.parent.mkdir(exist_ok=True)
        self.load_data()

    def load_data(self) -> None:
        """
        Load productivity data from file or initialize structure.
        """
        if self.data_file.exists():
            try:
                with open(self.data_file) as f:
                    self.data = json.load(f)
            except Exception:
                self.data = {
                    "sessions": [],
                    "languages": defaultdict(int),
                    "projects": defaultdict(int)
                }
        else:
            self.data = {
                "sessions": [],
                "languages": defaultdict(int),
                "projects": defaultdict(int)
            }

    def save_data(self) -> None:
        """
        Save productivity data to file.
        """
        try:
            # Convert defaultdicts to dicts for JSON serialization
            data_to_save = {
                "sessions": self.data["sessions"],
                "languages": dict(self.data["languages"]),
                "projects": dict(self.data["projects"])
            }
            with open(self.data_file, 'w') as f:
                json.dump(data_to_save, f)
        except Exception as e:
            print(f"Error saving data: {e}")

    def track_session(self, project: str, language: str, duration_minutes: int) -> None:
        """
        Track a coding session and update statistics.
        Args:
            project (str): Project name.
            language (str): Programming language.
            duration_minutes (int): Duration in minutes.
        """
        session = {
            "timestamp": datetime.now().isoformat(),
            "project": project,
            "language": language,
            "duration": duration_minutes
        }
        self.data["sessions"].append(session)
        self.data["languages"][language] += duration_minutes
        self.data["projects"][project] += duration_minutes
        self.save_data()

    def get_insights(self, days: int = 7) -> Dict[str, Any]:
        """
        Get productivity insights for the last N days.
        Args:
            days (int): Number of days to analyze.
        Returns:
            Dict[str, Any]: Insights and statistics.
        """
        cutoff = datetime.now() - timedelta(days=days)
        recent_sessions = [
            s for s in self.data["sessions"]
            if datetime.fromisoformat(s["timestamp"]) > cutoff
        ]
        total_time = sum(s["duration"] for s in recent_sessions)
        avg_session = total_time / len(recent_sessions) if recent_sessions else 0
        daily_totals = defaultdict(int)
        for session in recent_sessions:
            day = datetime.fromisoformat(session["timestamp"]).strftime("%A")
            daily_totals[day] += session["duration"]
        most_productive_day = max(daily_totals.items(), key=lambda x: x[1])[0] if daily_totals else "No data"
        return {
            "total_minutes": total_time,
            "average_session": round(avg_session, 1),
            "most_productive_day": most_productive_day,
            "top_languages": dict(sorted(self.data["languages"].items(), key=lambda x: x[1], reverse=True)[:3]),
            "active_projects": len(set(s["project"] for s in recent_sessions))
        }

tracker = ProductivityTracker()

@server.list_tools()
async def handle_list_tools() -> List[types.Tool]:
    """
    List available tools for productivity tracking.
    Returns:
        List[types.Tool]: List of tool definitions.
    """
    return [
        types.Tool(
            name="track_coding_session",
            description="Track a coding session",
            inputSchema={
                "type": "object",
                "properties": {
                    "project": {"type": "string"},
                    "language": {"type": "string"},
                    "duration_minutes": {"type": "integer"}
                },
                "required": ["project", "language", "duration_minutes"]
            }
        ),
        types.Tool(
            name="get_productivity_insights",
            description="Get productivity insights and statistics",
            inputSchema={
                "type": "object",
                "properties": {
                    "days": {"type": "integer", "default": 7}
                }
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> Any:
    """
    Execute a productivity tool operation.
    Args:
        name (str): Tool name.
        arguments (Dict[str, Any]): Tool arguments.
    Returns:
        Any: Result of the tool operation.
    Raises:
        ValueError: If the tool name is unknown.
    """
    if name == "track_coding_session":
        try:
            tracker.track_session(
                arguments["project"],
                arguments["language"],
                arguments["duration_minutes"]
            )
            return "Session tracked successfully."
        except Exception as e:
            return f"Error tracking session: {e}"
    elif name == "get_productivity_insights":
        try:
            days = arguments.get("days", 7)
            return tracker.get_insights(days)
        except Exception as e:
            return {"error": f"Error getting insights: {e}"}
    raise ValueError(f"Unknown tool: {name}")

# Example usage:
# tracker.track_session("projectX", "Python", 90)
# insights = tracker.get_insights(7)


