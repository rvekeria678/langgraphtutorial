from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage

from tools.iss_tool import get_astronaut_names, get_iss_location

from agents.base_agent import BaseAgent

def iss_agent(prompt: str) -> str:
    """
    Returns response from an ISS agent
    """
    tools = [get_astronaut_names, get_iss_location]
    llm = init_chat_model(model="gpt-3.5-turbo")
    sys_msg = SystemMessage(content="You are a helpful assistant that knows everything about the international space station (ISS)")

    agent = BaseAgent(tools=tools, llm=llm, system_message=sys_msg)

    return agent.run(prompt)