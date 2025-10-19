# STDIO-based server
# Dont use print statements! Writing to stdout will corrupt the JSON-RPC messages and break your server.

from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("mcp-lab")


def return_data():
    """ Finds some cool data """
    return "Cool data! Bobbys favorite color is orange-brown."

@mcp.tool()
def get_cool_data():
    """ Tool that returns some cool data """
    return return_data()

def main():
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()
