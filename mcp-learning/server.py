from mcp.server.fastmcp import FastMCP
from pathlib import Path
import requests

mcp=FastMCP("Demo")

@mcp.tool()
def github_list_files(repo_url:str):
    """ List all the directories and files present in the github repository link given by the user"""
    parts=repo_url.rstrip("/").split("/")

    owner=parts[-2]
    repo=parts[-1]
    url=f"https://api.github.com/repos/{owner}/{repo}/git/trees/main?recursive=1"
    res=requests.get(url)
    res.raise_for_status()
    data=res.json()

    return[
        item["path"] for item in data["tree"] if item["type"]=="blob"
    ]

@mcp.tool()
def search_files(keyword:str)->list[str]:
    """ This tool searches for project files with a matching keyword. Use this
        when the user does not explicitly know the files present in the project.
        The main purpose is to scan through the project files and retrieve the related files.     
       """
    proj_path=Path("demo-project")
    matches=[]
    for file in proj_path.rglob("*"):
        if not file.is_file():
            continue
        if keyword.lower() in file.name.lower():
            matches.append(str(file.relative_to(proj_path)))
            continue
        try:
            content=file.read_text(encoding='utf-8')

            if keyword.lower() in content.lower():
                matches.append(str(file))
        except Exception:
            continue
    return matches

@mcp.tool()
def read_file(file_path:str)->str:
    """ Read a file from the demo project.
        When the user explicitly asks for the content of a file use this 
    """
    proj_path=Path("demo-project").resolve()
    req_file=(proj_path/file_path).resolve()
    if not req_file.is_relative_to(proj_path):
        return "Access Denied"
    if not req_file.is_file():
        return "File Not Found"
    return req_file.read_text(encoding='utf-8')

@mcp.resource("project://info")
def get_info()->str:
    """ This is the resource providing information about the project"""
    return """
        Project: MCP Demo project

        Purpose:
        - To get a basic understanding of how mcp interacts and provide context.
        - How to use a mcp tool and resources.
        - Connecting it with a LLM.

        Current MCP Tools:
        - add()
        - multiply()

        current resources:
        - project://info

        Technology Stack:
        - Python
        - Google Gemini
        - modelcontextprotocol/sdk

        In the end this project is completely focussed on understanding the architecture of a MCP project.
        """

@mcp.prompt()
def explain_prompt()->str:
    """ This mcp prompt is used to generate a prompt for the llm for exact prompt."""
    return """
    Explain about this MCP project to the user. Cover the following points:

    - Explain what the project does.
    - Explain what MCP is
    - List what all tools are currently exposed and what they do?
    - List all the available resources
    - Also explain what are prompts
    """

if __name__=="__main__":
    mcp.run()