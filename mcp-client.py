# A simple mcp-client for testing

import asyncio
from typing import Optional
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class MCPClient:
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.llm = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

    async def connect_to_server(self, server_script_path: str):
        """Connect to an MCP server"""
        
        is_python = server_script_path.endswith('.py')
        if not (is_python):
            raise ValueError("Server script must be a .py file")
        
        command = "python"
        server_params = StdioServerParameters(
            command=command,
            args=[server_script_path],
            env=None
        )

        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))

        await self.session.initialize()

        response = await self.session.list_tools()
        tools = response.tools
        print("\nConnected to MCP server. Available tools:", [tool.name for tool in tools])

    async def process_query(self, query: str) -> str:
        """Process a query using OpenAI and available tools"""

        messages = [
            {
                "role": "user",
                "content": query
            }
        ]

        response = await self.session.list_tools()
        available_tools = [{
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.inputSchema
            }
        } for tool in response.tools]

        response = self.llm.chat.completions.create(
            model="qwen2.5:7b-instruct",
            max_tokens=1000,
            messages=messages,
            tools=available_tools,
            tool_choice="auto"
        )

        message = response.choices[0].message
        final_text = []

        if message.content:
            final_text.append(message.content)

        if message.tool_calls:
            messages.append({
                "role": "assistant", 
                "content": message.content,
                "tool_calls": message.tool_calls
            })

            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                import json
                tool_args = json.loads(tool_call.function.arguments)

                final_text.append(f"[Calling tool {tool_name} with args {tool_args}]")

                result = await self.session.call_tool(tool_name, tool_args)
                
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result.content)
                })

            final_response = self.llm.chat.completions.create(
                model="qwen2.5:7b-instruct",
                max_tokens=1000,
                messages=messages,
                tools=available_tools,
                tool_choice="auto"
            )

            final_message = final_response.choices[0].message
            if final_message.content:
                final_text.append(final_message.content)
        
        return "\n".join(final_text)
    
    async def chat_loop(self):
        """Run an interactive chat loop"""

        print("\nMCP Client started!")
        print("Type something, and 'quit' to exit.")

        while True:
            try:
                query = input("\nQuery: ").strip()
                if query.lower() == "quit":
                    print("Bye bye!")
                    break

                response = await self.process_query(query)
                print("\n" + response)

            except Exception as e:
                print(f"Error: {e}")

    async def cleanup(self):
        """Cleanup resources"""
        await self.exit_stack.aclose()

async def main():
    if len(sys.argv) < 2:
        print("Usage: python mcp-client.py <path_to_mcp_server_script>")
        sys.exit(1)

    client = MCPClient()
    try:
        await client.connect_to_server(sys.argv[1])
        await client.chat_loop()
    finally:
        await client.cleanup()

if __name__ == "__main__":
    import sys
    asyncio.run(main())