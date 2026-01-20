"""
Import necessary modules and define the State representation for the configuration builder.
"""
from pydantic import BaseModel, Field
from langchain.tools import tool

class DatabaseConfig(BaseModel):
    """Database configuration details."""
    db_type: str = Field(..., description="Type of the database (e.g., PostgreSQL, MySQL)")
    port: int = Field(..., description="Database port number")
    username: str = Field(..., description="Username for database authentication")
    password: str = Field(..., description="Password for database authentication")
    database_name: str = Field(..., description="Name of the database")

@tool
def config_builder():   
    """
    Interactive tool to build and save database configuration files.
    """
    while True:
        print("Please provide the following database configuration details:")

        db_type=input("Input Database TYPE (e.g., PostgreSQL, MySQL): ")
        port=int(input("Input Database PORT number: "))
        username=input("Input USERNAME for database authentication: ")
        password=input("Input PASSWORD for database authentication: ")
        database_name=input("Input DATABASE NAME: ")
    
        config=DatabaseConfig(
        db_type=db_type,
        port=port,
        username=username,
        password=password,
        database_name=database_name
            )
        print("Please confirm the following configuration details:",config)
        confirm=input("Confirm (yes/y to save, q to quit): ")
        if confirm.lower() in ["yes","y"]:
            with open(f"temp/{config.db_type}.{config.database_name}.config","w") as file:
                file.write(config.model_dump_json())
            return f"temp/{config.db_type}.{config.database_name}.config"
        elif confirm.lower() in ["q","Q"]:
            print("Exiting config builder.")
            return "Exited config builder without saving."
        else:
            print("Invalid input. Please enter 'yes', 'y', 'q', or 'Q'.")
