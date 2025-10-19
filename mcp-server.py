# STDIO-based server
# Dont use print statements! Writing to stdout will corrupt the JSON-RPC messages and break your server.

from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("mcp-lab")

random_cool_data = [
    "Cool data! Alice's favorite color is blue.",
    "Cool data! Charlie loves hiking in the mountains.",
    "Cool data! Eve enjoys painting abstract art.",
    "Cool data! Dave is a big fan of jazz music.",
    "Cool data! Frank collects vintage comic books."
]

def return_data(random_number: int) -> str:
    """ Finds some cool data """
    if 0 <= random_number < len(random_cool_data):
        return random_cool_data[random_number]
    return "Cool data not found."

@mcp.tool()
def get_cool_data(random_number: int) -> str:
    """ Tool that returns some cool data 
    
    Args:
        random_number (int): A random number between 0 and 4 to select the cool data.
    """
    
    return return_data(random_number)

def main():
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()
