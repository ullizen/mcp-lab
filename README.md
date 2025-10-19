# mcp-lab
Playground for trying out mcp servers

## Test with claude desktop
1. Add your mcp-server to claude desktop config:

```
{
  "mcpServers": {
    "mcp-lab": {
      "command": "uv",
      "args": [
        "--directory",
        "/PATH/TO/mcp-lab",
        "run",
        "mcp-server.py"
      ]
    }
  }
}
```
* use absolute path for uv binary if you get the error ´spawn uv ENOENT´

2. See that the mcp-server is available in claud desktop (under search and tools)

3. Ask a question, and see if it uses your mcp-server to create a response!

## Resources
- MCP docs - Build an MCP server: https://modelcontextprotocol.io/docs/develop/build-server
