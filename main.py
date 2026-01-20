from langchain_core import messages
from langchain_core.messages import tool
from langchain_core.messages import ToolMessage
from pydantic import BaseModel
from typing import Optional, TypedDict, Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
import os
import dotenv

from configbuilder import config_builder

dotenv.load_dotenv()

system_prompt=ChatPromptTemplate.from_messages(
    [
        ("system",
         """
            You are a helpuful chatbot and will assist the users in problems and queries relating to database.
            It can be queries writing,understanding or concept explanation.
            You may also be asked to run a tool for database config creation.
            Keep the answers concise and to the point. Keep token count as low as possible.
        """
        ),
        (
            "placeholder","{messages}",
        ),
    ]
)
# system_prompt="""
#         You are a helpuful chatbot and will assist the users in problems and queries relating to database.
#         It can be queries writing,understanding or concept explanation.
#         You may also be asked to run a tool for database config creation.
#         Keep the answers concise and to the point. Keep token count as low as possible.
#     """


llm=init_chat_model(
    model="openai/gpt-oss-20b",
    api_key=os.environ["LLM_API_KEY"],
    model_provider="openai",
    base_url="https://openrouter.ai/api/v1"
)
tools=[config_builder]
llm_with_tools=llm.bind_tools(tools)
chatAgent=system_prompt | llm_with_tools

class State(TypedDict):
    """State representation for the main chatbot."""
    messages: Annotated[list, add_messages]
    # user_input: Optional[str]
    tools: Optional[list]
    end: bool

def chatbot(state: State):
    messages=state["messages"]
    
    response=chatAgent.invoke({"messages":messages})
    # Assuming response is an AIMessage with tool_calls or content
    state["messages"].append(response)
    # Print the bot's response
    if response.content:
        print("Bot:", response.content)
    return state

def tool_runner(state: State):
    """Run the tool if any tool invocation is present in the messages."""
    print("Running tool runner...")
    messages=state["messages"]
    last_message=messages[-1]
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        for tool_call in last_message.tool_calls:
            tool_name=tool_call["name"]
            for tool in tools:
                if tool.name==tool_name:
                    tool_response=tool.invoke(tool_call["args"])
                    messages.append(ToolMessage(
                        content=tool_response,
                        name=tool_name,
                        tool_call_id=tool_call["id"]
                    ))
    return state

def get_input(state: State):
    user_input = input("You: ")
    if user_input.lower() == "end":
        state["end"] = True
    else:
        state["messages"].append({"role": "user", "content": user_input})
    return state

# Define the workflow graph directly in main.py
def workflow_graph():
    workflow = StateGraph(state_schema=State)

    workflow.add_node("chatbot", chatbot)
    workflow.add_node("tool_runner", tool_runner)
    workflow.add_node("get_input", get_input)

    workflow.add_edge(START, "get_input")
    workflow.add_conditional_edges("get_input", input_router, {"continue": "chatbot", "end": END})
    workflow.add_conditional_edges("chatbot", router, {"tool": "tool_runner", "continue": "get_input"})
    workflow.add_edge("tool_runner", "chatbot")

    return workflow.compile()

def router(state: State):
    last_message = state["messages"][-1] if state["messages"] else None
    if last_message and hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        return "tool"
    else:
        return "continue"

def input_router(state: State):
    return "end" if state.get("end", False) else "continue"

# Initialize the workflow graph
graph = workflow_graph()


# Run the workflow
def run_workflow():
    state = State(messages=[], tools=tools, end=False)
    graph.invoke(state)

if __name__ == "__main__":
    run_workflow()



