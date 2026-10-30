
import asyncio
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "app.mcp_server"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            print("MCP Connection Successful")

            print("\n--- Test 1: Ticket Lookup ---")
            ticket = await session.call_tool(
                "get_ticket_status_mcp",
                {"ticket_id": "TCK-1001"},
            )

            for item in ticket.content:
                if hasattr(item, "text"):
                    print(item.text)

            print("\n--- Test 2: Policy Search ---")
            policy = await session.call_tool(
                "search_policies_mcp",
                {"query": "PTO policy"},
            )

            for item in policy.content:
                if hasattr(item, "text"):
                    print(item.text)


if __name__ == "__main__":
    asyncio.run(main())
