from dotenv import load_dotenv
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import tools_condition, ToolNode
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

load_dotenv()

class BaseAgent:
    def __init__(self, tools: list, llm, system_message: SystemMessage):
        """
        Wrapper around LangGraph agent.
        Args:
            tools (list): List of tool functions for arithmetic or other tasks.
            llm: an initialized LangChain chat model (e.g., GPT-3.5-turbo)
            system_message (SystemMessage): System instructions for the agent.
        """
        self.tools = tools
        # Bind the tools to the LLM
        self.llm_with_tools = llm.bind_tools(tools)
        self.system_message = system_message
        # Build the graph
        self._build_graph()

    def _assistant_node(self, state: MessagesState):
        # Prepend system message and invoke model
        messages = [self.system_message] + state["messages"]
        response = self.llm_with_tools.invoke(messages)
        tool_calls = response.additional_kwargs.get("tool_calls", [])
        print(f"[DEBUG] Assistant response: {tool_calls}\n")
        return {"messages": state["messages"] + [response]}
    
    def _build_graph(self):
        builder = StateGraph(MessagesState)
        # Assistant node
        builder.add_node("assistant", self._assistant_node)
        # Tools node for confitional execution
        builder.add_node("tools", ToolNode(self.tools))
        # Edges setup
        builder.add_edge(START, "assistant")
        builder.add_conditional_edges("assistant", tools_condition)
        builder.add_edge("tools", "assistant")
        # Compile the graph
        self.graph = builder.compile()

    def run(self, user_input: str):
        """
        Executes the agent for a single human input and returns the AI's reply
        Args:
            user_input (str): The user's human input and returns the AI's reply.
        Returns:
            str: The AI assistant's reponse.
        """
        initial_state = {"messages": [HumanMessage(content=user_input)]}
        final_state = self.graph.invoke(initial_state)
        ai_messages = [msg for msg in final_state["messages"] if isinstance(msg, AIMessage)]
        
        if ai_messages:
            return ai_messages[-1].content
        return None