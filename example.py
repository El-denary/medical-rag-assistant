from state import State
from workflow import Workflow
from dotenv import load_dotenv
load_dotenv()


intial_state = State(
  {
    "query": "what is diabetes ?",
    "messages": [],
    "content": None,
    "response": None,
    "rewritten_query": None
  }
)

workflow = Workflow()
result = workflow.run(intial_state)

print(f"rewritten query: {result.get('rewritten_query')}")
print ("--"* 50)

print(f"response: {result.get('response')}")
