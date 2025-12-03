import asyncio
import os
from langchain_mcp_adapters.client import MultiServerMCPClient
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


load_dotenv()

SERVERS = {
    "maths_cal": {
        "transport": "stdio",
        "command": "C:/Users/Ravi0dubey/anaconda3/Scripts/uv.exe",
        "args": [
            "run",
            "--with",
            "fastmcp",
            "fastmcp",
            "run",
            "D:\\Study\\Data Science\\MCP\\5_MCP_client_project\\5_1_mcp_local_server\\main.py"

      ]
    },
}

async def main():
    # initialize the MultiserverMCPClient with server address
    client = MultiServerMCPClient(SERVERS)
    tools = await client.get_tools()
    named_tools ={}
    for tool in tools:
        named_tools[tool.name] = tool

    llm= ChatOpenAI(model= "gpt-5", api_key=os.getenv("OPEN_API_KEY"))   
    llm_with_tools = llm.bind_tools(tools)

    prompt1 = "What is the sum of 15.5 and 24.3 using maths_cal tool?"
    
    response = await llm_with_tools.ainvoke(prompt1)
    selected_tool = response.tool_calls[0]["name"]
    selected_tool_args = response.tool_calls[0]["args"]
    
    # print(f"selected_tool: {selected_tool}\n")
    # print(f"selected_tool_args: {selected_tool_args}\n")

    tool_result1 = await named_tools[selected_tool].ainvoke(selected_tool_args)
    print(f"Q: {prompt1}\nA: {tool_result1}\n")

if __name__ == '__main__':
    asyncio.run(main())