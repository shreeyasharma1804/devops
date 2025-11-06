from fastmcp import FastMCP
from typing import Annotated
import os
from fastmcp.exceptions import ToolError

mcp = FastMCP(name="ReadFile", strict_input_validation=True)


@mcp.tool()
def ReadFileUsingLLM(path: Annotated[str, "path of the file to read"]) -> str:
    """Read a file using LLM.

    Args:
        path (str): The path to the file to be read. Provide the full path

    Returns:
        str: The contents of the file.
    """

    if not os.path.exists(path):
        raise ToolError("Path not found")

    with open(path, "r") as file:
        content = file.read()

    return content


if __name__ == "__main__":
    mcp.run(transport="sse",
            host="localhost",
            port=8000)
