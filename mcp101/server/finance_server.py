#finance_server.py
from mcp.server.fastmcp import FastMCP
import random

# Create a simple finance MCP server
mcp = FastMCP("finance")

@mcp.tool()
def calculate_profit(revenue: float, expenses: float, tax_rate: float = 0.2) -> dict:
    """Calculate profit using a simple equation with random factor"""
    # Add a random market factor between -5% and +10%
    market_factor = 1 + random.uniform(-0.05, 0.1)
    
    # Basic profit calculation with tax and market factor
    gross_profit = revenue - expenses
    taxed_profit = gross_profit * (1 - tax_rate)
    final_profit = taxed_profit * market_factor
    
    return {
        "profit": round(final_profit, 2),
        "formula": "Profit = (Revenue - Expenses) * (1 - Tax Rate) * Market Factor",
        "market_factor": round(market_factor, 2)
    }

@mcp.tool()
def calculate_cost(base_cost: float, quantity: int) -> dict:
    """Calculate total cost with bulk discount"""
    # Apply random discount based on quantity
    discount = min(0.3, quantity / 1000) 
    
    # Basic cost calculation with discount
    total_cost = base_cost * quantity * (1 - discount)
    
    return {
        "cost": round(total_cost, 2),
        "formula": "Cost = Base Cost * Quantity * (1 - Discount)",
        "discount_percent": round(discount * 100, 1)
    }

if __name__ == "__main__":
    mcp.run()