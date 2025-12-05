import asyncio
import os
from langchain_mcp_adapters.client import MultiServerMCPClient
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import ToolMessage


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

    prompt = "What is the sum of 15.5 and 24.3 using maths_cal tool?" 
    response = await llm_with_tools.ainvoke(prompt)

    selected_tool = response.tool_calls[0]["name"]
    selected_tool_args = response.tool_calls[0]["args"]
    selected_tool_id = response.tool_calls[0]["id"]
    
    tool_result = await named_tools[selected_tool].ainvoke(selected_tool_args)
    
    tool_message = ToolMessage(content=str(tool_result),  tool_call_id=selected_tool_id)

    final_response = await llm_with_tools.ainvoke([prompt, response, tool_message])
    print(f"Final Response: {final_response.content}")

if __name__ == '__main__':
    asyncio.run(main())