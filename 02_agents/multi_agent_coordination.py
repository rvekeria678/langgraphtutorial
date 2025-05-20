from langgraph.graph import StateGraph, END
from langchain_core.runnables import Runnable
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

# --- Define the state type ---
from typing import TypedDict, Optional

class GraphState(TypedDict):
    topic: str
    research: Optional[str]
    summary: Optional[str]

# --- Define Agent A: Researcher ---
class ResearchAgent(Runnable):
    def invoke(self, state: GraphState) -> GraphState:
        topic = state["topic"]

        mock_data = f"Research on {topic}: It is a fascinating subject with many facets..."
        return {"topic": topic, "research": mock_data}

# --- Define Agent B: Writer ---
class WritingAgent(Runnable):
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4", temperature=0)

    def invoke(self, state: GraphState) -> GraphState:
        research = state["research"]
        prompt = f"Summarize this research for a layperson:\n\n{research}"
        response = self.llm.invoke(prompt)
        return {"topic": state["topic"], "research": research, "summary": response.content}

# --- Build the Graph ---
researcher = ResearchAgent()
writer = WritingAgent()

graph = StateGraph(GraphState)
graph.add_node("research_node", researcher)
graph.add_node("write", writer)

graph.set_entry_point("research_node")
graph.add_edge("research_node", "write")
graph.add_edge("write", END)

app = graph.compile()

# --- Run it ---
if __name__ == "__main__":
    input_state = {"topic": "quantum computing"}
    result = app.invoke(input_state)
    print("Final Output:")
    print(result["summary"])