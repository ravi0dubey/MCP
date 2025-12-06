import asyncio
import os
import json
from langchain_mcp_adapters.client import MultiServerMCPClient
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import ToolMessage


load_dotenv()

# Step 1: Define MCP Servers
#    1.1: First server is maths_cal (local server) running on stdio transport used for mathematical calculations
#    1.1: Second server is  expense tracker (local server) running on stdio transport used for expense tracking
#    1.1: Third server is expense tracker  (MCP server) running on streamable_http used for expense tracking

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
    "Demo Server": {
      "transport": "stdio",
      "command": "C:/Users/Ravi0dubey/anaconda3/Scripts/uv.exe",
      "args": [
        "run",
        "--with",
        "fastmcp",
        "fastmcp",
        "run",
        "D:\\Study\\Data Science\\MCP\\2_MCP_local_server\\1_expense_tracker_mcp_server\\main.py"
      ],
      "env": {},
    },
    "Ravi Dubey Proxy server": {
      "transport": "streamable_http",
      "url": "https://ravidubey-expensetracker.fastmcp.app/mcp",
    }
  }

# Step 2: Create MCP Client and connect with the MCP Servers. 
#    2.1: Retrieve the list of available tools and save them in a dictionary for easy access later.
async def main():
    # initialize the MultiserverMCPClient with server address
    client = MultiServerMCPClient(SERVERS)
    tools = await client.get_tools()
    named_tools ={}
    for tool in tools:
        named_tools[tool.name] = tool
    print (f"Available tools are: {list(named_tools.keys())}")
# Step 3: Initialize LLM and bind tools
    llm= ChatOpenAI(model= "gpt-5", api_key=os.getenv("OPEN_API_KEY"))   
    llm_with_tools = llm.bind_tools(tools)

# Step 4: Give prompt to the LLM with tools and get response.
    prompt = "What is the quotient of 151.5 divided  7.3 using maths_cal tool?" 
    # prompt = "Who is hosting fifa world cup 2026?" 
    prompt = "Add and track an expense of $45 for groceries in my expense tracker using Ravi Dubey Proxy server tool."
    response = await llm_with_tools.ainvoke(prompt)

# Step 5: If there is no tool call, print normal LLM response
    if not getattr(response, "tool_calls", None):
        print(f"Response from LLM : {response.content}")
        return

# Step 6: If there are tool calls, execute them and send results back to LLM for final response  
#    6.1: Loops over each tool call (GPT-5 can call multiple tools in one response).
#    6.2: Runs the actual MCP tool with the arguments GPT-5 provided.
#    6.3: Creates a ToolMessage that sends the tool’s output back to GPT-5
    tool_message  = []
    for tool_call in response.tool_calls:      
        selected_tool = tool_call["name"]
        selected_tool_args = tool_call["args"] or {}
        selected_tool_id = tool_call["id"]
        result = await named_tools[selected_tool].ainvoke(selected_tool_args)
        tool_message.append(ToolMessage(tool_call_id=selected_tool_id, content=json.dumps(result)))

# Step 7: Send the tool results back to LLM for final response
#      7.1 : The prompt is also sent back to provide context.
#      7.2 : The original response from LLM is also sent back to provide context.
#      7.3 : The tool messages containing the tool results are also sent back.

    final_response = await llm_with_tools.ainvoke([prompt, response, *tool_message])
    print(f"Response from LLM Tool is : {final_response.content}")

if __name__ == '__main__':
    asyncio.run(main())