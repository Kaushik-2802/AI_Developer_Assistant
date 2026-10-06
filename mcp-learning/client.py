import asyncio

from mcp import ClientSession,StdioServerParameters
from mcp.client.stdio import stdio_client

server_params=StdioServerParameters(command="python",args=["server.py"])

async def main():
    async with stdio_client(server_params) as (read,write):
        async with ClientSession(read,write) as session:
            await session.initialize()
            tools= await session.list_tools()
            print("Available tools:")
            for tool in tools.tools:
                print(f"- {tool.name}")
                print(f" Description: {tool.description}")
                print(f" Input Schema: {tool.inputSchema}")
            result=await session.call_tool(
                "add",
                arguments={"a":10,"b":20}
            )
            print("Tool res:",result)

if __name__=="__main__":
    asyncio.run(main())