from fastmcp import FastMCP

# Create a proxy to your FastMCP Cloud Server
# FastMCP Cloud uses Streamable HTTP (default), so copy your remote MCPURL from fastMCP.cloud
mcp = FastMCP.as_proxy(
    "https://ravidubey-expensetracker.fastmcp.app/mcp",
    name = "Ravi Dubey Proxy server"
)


if __name__ == "__main__":
   # This runs via STDIO, which Claude Desktop can connect to
   mcp.run()


