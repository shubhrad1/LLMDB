def ConfigReader(path:str)->str:
    # filepath="temp/PostgreSQL.banana.config"
    try:
        with open(path, "r",encoding="utf-8") as file:
            content=file.read()
            return content
    except FileNotFoundError:
        return "Config file not found. Please create a config first."


    
