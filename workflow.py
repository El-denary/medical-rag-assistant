from agents import *
from state import State
from langgraph.graph import StateGraph , START , END

class Workflow:
  def __init__(self):
     self.rewrite = rewritten_query_agent
     self.retrieve = retriever_agent
     self.respond = response_agent

  def build_graph(self):
      graph = StateGraph(State)

      #  nodes
      graph.add_node("rewrite_query", self.rewrite)
      graph.add_node("retrieve_documents", self.retrieve)
      graph.add_node("generate_response", self.respond)

        # edges
      graph.add_edge(START, "rewrite_query")
      graph.add_edge("rewrite_query", "retrieve_documents")
      graph.add_edge("retrieve_documents", "generate_response")
      graph.add_edge("generate_response", END)

      return graph.compile()
  
  def run(self, initial_state: State):
      graph = self.build_graph()
      result = graph.invoke(initial_state)
      return result
     

     