from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage

from tools.calculator_tools import add, subtract, multiply, divide
from tools.iss_tool import get_astronaut_names, get_iss_location
from tools.time_tool import current_time, is_dark_outside, get_current_location, get_timezone

from agents.base_agent import BaseAgent

if __name__ == "__main__":
    tools = [get_astronaut_names, get_iss_location] + [current_time, is_dark_outside, get_current_location, get_timezone]
    llm = init_chat_model(model="gpt-3.5-turbo")
    sys_msg = SystemMessage(content="You are a helpful assistant that knows everything about the international space station (ISS)")

    agent = BaseAgent(tools=tools, llm=llm, system_message=sys_msg)

    while True:
        user_input = input("You: ")
        if user_input.lower() in ("exit", "quit"):
            break
        response = agent.run(user_input)
        print(f"Assistant: {response}")