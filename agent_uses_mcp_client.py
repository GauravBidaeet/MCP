# refer to "https://reference.langchain.com/python/langchain-mcp-adapters"

import os
import asyncio
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_ollama import ChatOllama
# ollama run qwen3.5:2b

load_dotenv()

async def run_agent():
    print("RUN_AGENT STARTED")
    client = MultiServerMCPClient(
        {
            "bright_data": {
                "command": "npx",
                "args": ["@brightdata/mcp"],
                "env": {
                    "API_TOKEN": os.getenv("BRIGHT_DATA_API_TOKEN")
                },
                "transport": "stdio",
            },
        }
    )
    tools = await client.get_tools()
    model = ChatOllama(model="qwen3.5:2b")
    agent = create_agent(model, tools, system_prompt="Your are a web search agent with access to bright data tool to get latest data")
    agent_response = await agent.ainvoke({"messages": "who won ipl 2025?"})
    print(agent_response["messages"][-1].content)

if __name__ == "__main__":
    asyncio.run(run_agent())