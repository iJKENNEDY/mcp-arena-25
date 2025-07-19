from typing import List, Dict, Any, Optional

from mcp.server import Server
import mcp.types as types

from pathlib import Path

import json
import hashlib

from datetime import datetime

server = Server("ml-experimental-tracker")

class ExperimentTracker:
    """
    Tracks and compares machine learning experiments.
    """
    def __init__(self) -> None:
        self.experiments_file = Path.home() / '.mcp' / 'ml_experiments.json'
        self.load_experiments()

    def load_experiments(self) -> None:
        """
        Load experiments from file or initialize empty list.
        """
        if self.experiments_file.exists():
            try:
                with open(self.experiments_file) as f:
                    self.experiments = json.load(f)
            except Exception:
                self.experiments = []
        else:
            self.experiments = []

    def save_experiments(self) -> None:
        """
        Save experiments to file.
        """
        try:
            with open(self.experiments_file, 'w') as f:
                json.dump(self.experiments, f)
        except Exception as e:
            print(f"Error saving experiments: {e}")

    def log_experiment(self, name: str, model_type: str, hyperparams: Dict[str, Any],
                      metrics: Dict[str, Any], dataset: str, notes: str = "") -> str:
        """
        Log a new experiment and return its ID.
        Args:
            name (str): Experiment name.
            model_type (str): Model type.
            hyperparams (Dict[str, Any]): Hyperparameters.
            metrics (Dict[str, Any]): Metrics.
            dataset (str): Dataset name.
            notes (str): Optional notes.
        Returns:
            str: Experiment ID.
        """
        experiment = {
            "id": hashlib.md5(f"{name}{datetime.now()}".encode()).hexdigest()[:8],
            "timestamp": datetime.now().isoformat(),
            "name": name,
            "model_type": model_type,
            "hyperparameters": hyperparams,
            "metrics": metrics,
            "dataset": dataset,
            "notes": notes
        }
        self.experiments.append(experiment)
        self.save_experiments()
        return experiment["id"]

    def compare_experiments(self, experiment_ids: List[str], metric: str) -> List[Dict[str, Any]]:
        """
        Compare experiments by a specific metric.
        Args:
            experiment_ids (List[str]): List of experiment IDs.
            metric (str): Metric to compare.
        Returns:
            List[Dict[str, Any]]: Sorted comparison results.
        """
        results = []
        for exp in self.experiments:
            if exp["id"] in experiment_ids:
                results.append({
                    "id": exp["id"],
                    "name": exp["name"],
                    "model": exp["model_type"],
                    metric: exp["metrics"].get(metric, "N/A")
                })
        return sorted(results, key=lambda x: x[metric] if isinstance(x[metric], (int, float)) else 0, reverse=True)

    def find_best_hyperparams(self, model_type: str, metric: str, maximize: bool = True) -> Optional[Dict[str, Any]]:
        """
        Find best hyperparameters for a model type by metric.
        Args:
            model_type (str): Model type.
            metric (str): Metric to optimize.
            maximize (bool): Whether to maximize or minimize the metric.
        Returns:
            Optional[Dict[str, Any]]: Best experiment info or None.
        """
        relevant_exps = [e for e in self.experiments if e["model_type"] == model_type]
        if not relevant_exps:
            return None
        best = max(relevant_exps, key=lambda e: e["metrics"].get(metric, 0)) if maximize else \
               min(relevant_exps, key=lambda e: e["metrics"].get(metric, float('inf')))
        return {
            "experiment_id": best["id"],
            "hyperparameters": best["hyperparameters"],
            "metric_value": best["metrics"].get(metric)
        }

tracker = ExperimentTracker()

@server.list_tools()
async def handle_list_tools() -> List[types.Tool]:
    """
    List available tools for experiment tracking.
    Returns:
        List[types.Tool]: List of tool definitions.
    """
    return [
        types.Tool(
            name="log_ml_experiment",
            description="Log a machine learning experiment",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "model_type": {"type": "string"},
                    "hyperparameters": {"type": "object"},
                    "metrics": {"type": "object"},
                    "dataset": {"type": "string"},
                    "notes": {"type": "string"}
                },
                "required": ["name", "model_type", "hyperparameters", "metrics", "dataset"]
            }
        ),
        types.Tool(
            name="compare_experiments",
            description="Compare multiple experiments by a specific metric",
            inputSchema={
                "type": "object",
                "properties": {
                    "experiment_ids": {"type": "array", "items": {"type": "string"}},
                    "metric": {"type": "string"}
                },
                "required": ["experiment_ids", "metric"]
            }
        ),
        types.Tool(
            name="find_best_hyperparameters",
            description="Find best hyperparameters for a model type",
            inputSchema={
                "type": "object",
                "properties": {
                    "model_type": {"type": "string"},
                    "metric": {"type": "string"},
                    "maximize": {"type": "boolean", "default": True}
                },
                "required": ["model_type", "metric"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> Any:
    """
    Execute an experiment tracking tool operation.
    Args:
        name (str): Tool name.
        arguments (Dict[str, Any]): Tool arguments.
    Returns:
        Any: Result of the tool operation.
    Raises:
        ValueError: If the tool name is unknown.
    """
    if name == "log_ml_experiment":
        try:
            exp_id = tracker.log_experiment(
                arguments["name"],
                arguments["model_type"],
                arguments["hyperparameters"],
                arguments["metrics"],
                arguments["dataset"],
                arguments.get("notes", "")
            )
            return {"experiment_id": exp_id}
        except Exception as e:
            return {"error": f"Error logging experiment: {e}"}
    elif name == "compare_experiments":
        try:
            return tracker.compare_experiments(
                arguments["experiment_ids"],
                arguments["metric"]
            )
        except Exception as e:
            return {"error": f"Error comparing experiments: {e}"}
    elif name == "find_best_hyperparameters":
        try:
            result = tracker.find_best_hyperparams(
                arguments["model_type"],
                arguments["metric"],
                arguments.get("maximize", True)
            )
            return result if result else {"error": "No experiments found for given model type."}
        except Exception as e:
            return {"error": f"Error finding best hyperparameters: {e}"}
    raise ValueError(f"Unknown tool: {name}")

# Example usage:
# tracker.log_experiment("exp1", "RandomForest", {"n_estimators": 100}, {"accuracy": 0.92}, "iris")
# tracker.compare_experiments(["id1", "id2"], "accuracy")
# tracker.find_best_hyperparams("RandomForest", "accuracy", True)

