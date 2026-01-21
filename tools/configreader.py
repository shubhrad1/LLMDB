from langchain.tools import tool

@tool
def ConfigReader(path:str)->str:
    """
    Reads the database configurations from the specified config file.
    Args:
    path: Path to the configuration file.
    Returns:
    The content of the configuration file as a string.
    """
    # filepath="temp/PostgreSQL.banana.config"
    try:
        with open(path, "r",encoding="utf-8") as file:
            content=file.read()
            return content
    except FileNotFoundError:
        return "Config file not found. Please create a config first."
