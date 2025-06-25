#finance_client.py
import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    # Configure server connection
    server_params = StdioServerParameters(
        command="python",
        args=["finance_server.py"],
        cwd=""
    )

    # Start the server and create read/write streams
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            print("Connected to Finance MCP server!")
            
            # Calculate profit
            profit_result = await session.call_tool("calculate_profit", arguments={
                "revenue": 100000,
                "expenses": 75000,
                "tax_rate": 0.2
            })
            
            # Extract the response data - handle only if 'text' attribute exists
            profit_content = profit_result.content[0]
            profit_json = getattr(profit_content, "text", None)
            if profit_json is None:
                print("Error: El contenido de profit no tiene atributo 'text'. Tipo:", type(profit_content))
                return
            profit_data = json.loads(profit_json)
            
            print(f"\nProfit: ${profit_data['profit']}")
            print(f"Formula: {profit_data['formula']}")
            print(f"Market Factor: {profit_data['market_factor']}")
            
            # Calculate cost
            cost_result = await session.call_tool("calculate_cost", arguments={
                "base_cost": 50,
                "quantity": 500
            })
            # Extract the response data - handle only if 'text' attribute exists
            cost_content = cost_result.content[0]
            cost_json = getattr(cost_content, "text", None)
            if cost_json is None:
                print("Error: El contenido de cost no tiene atributo 'text'. Tipo:", type(cost_content))
                return
            cost_data = json.loads(cost_json)
            
            print(f"\nCost: ${cost_data['cost']}")
            print(f"Formula: {cost_data['formula']}")
            print(f"Discount: {cost_data['discount_percent']}%")

if __name__ == "__main__":
    asyncio.run(main())