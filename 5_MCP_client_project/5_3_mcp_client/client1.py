from asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient

async def main():
    print(' ')
    # initialize the MultiserverMCPClient with server address
    client = MultiServerMCPClient(
        server_address=[]
    )

if __name__ == '__main__':
    asyncio.run(main())