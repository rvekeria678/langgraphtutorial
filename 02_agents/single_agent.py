from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool

# ----- TOOL DEFINITION ----- #
@tool
def magic_function(input: int) -> int:
    """function returns double the input."""
    print(">:(magic_function invoked)")
    return input * 2

# ----- LLM SETUP ----- #
model = ChatOpenAI(model="gpt-3.5-turbo")
tools = [magic_function]

# ----- AGENT SETUP ----- #
react_agent = create_react_agent(
    model=model,
    tools=tools
)

# ----- AGENT EXECUTION ----- #
for step in react_agent.stream({"messages":[("human", "what is the value of magic_function(3)?")]}, stream_mode="updates"):
    print(step['messages'])