import asyncio
from fastmcp import Client, FastMCP
from fastmcp.exceptions import ToolError


client = Client("http://localhost:8000/sse")

async def main():

    async with client:

        await client.ping()

        try:

            # List all the tools
            
            # tools = await client.list_tools()

            result = await client.call_tool("ReadFileUsingLLM", {"path": "/Users/shreeya/Documents/devops/mcp_servers/read_files/server.py"})
            print(result.structured_content['result'])

        except ToolError as e:
            print(f"ToolError: {e}")

asyncio.run(main())
