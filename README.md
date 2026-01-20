# LLMDB

LLMDB is a prototype tool designed to create database configurations, use Docker to set up database infrastructure, and execute database queries through a natural language interface.

## Features

- Interactive conversation for database assistance
- Tool for creating and saving database configuration files
- Planned: Docker-based database infrastructure setup
- Planned: Natural language query execution

## Current Functionality

- Chat about database concepts
- Use config builder tool to build config files

## Installation

1. Clone the repository:

    ```
    git clone https://github.com/shubhrad1/LLMDB.git
    cd LLMDB
    ```

2. Install dependencies:

    ```
    pip install -r requirements.txt
    ```

3. Set up environment variables:
   Create a `.env` file in the root directory with:
    ```
    LLM_API_KEY=your_openai_api_key_here
    ```

## Usage

Run the chatbot:

```
python main.py
```

Interact with the chatbot by typing queries related to databases. Type "end" to exit.

Currently, the chatbot can answer questions about database concepts and generate database configurations via the config_builder tool.

## Configuration

- The chatbot uses the "openai/gpt-oss-20b" model via OpenRouter.
- Configuration files are saved in the `temp/` directory.
- Modify `main.py` to change the model or API settings.

## Project Structure

- `main.py`: Main application with the LangGraph workflow
- `configbuilder.py`: Tool for database configuration creation
- `requirements.txt`: Python dependencies
- `temp/`: Directory for generated config files

## License

This project is licensed under the MIT License.
